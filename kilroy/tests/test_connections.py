import unittest
from kilroy import DiscordConnection, DiscordMessage, DiscordChannel
import asyncio
from concurrent.futures import FIRST_COMPLETED


class TestConnection:

    CONNECTION_CLASS = None
    MESSAGE_CLASS = None
    CHANNEL_CLASS = None

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_message_class(self):
        self.assertIs(self.CONNECTION_CLASS.get_message_class(),
                        self.MESSAGE_CLASS)

    def test_channel_class(self):
        self.assertIs(
            self.CONNECTION_CLASS.get_message_class().get_channel_class(),
            self.CHANNEL_CLASS
            )

    def test_send_and_receive_message(self):
        MESSAGE = "Hello Discord"
        MESSAGE_TIMEOUT_SECONDS = 5
        MESSAGE_TIMEOUT_PET = .2
        received_message = False

        connection = self.CONNECTION_CLASS()

        async def message_listener(message):
            # Check if the test message came in
            if message.text == MESSAGE:
                received_message = True

        async def go():
            await connection.await_until_connected()
            connection.add_message_listener(message_listener)
            await connection.send_message_text(MESSAGE)

            message = connection.get_message_class()

            # Spin until the message listener signals that we're done
            elapsed = 0
            while (not received_message) and (elapsed < MESSAGE_TIMEOUT_SECONDS):
                elapsed += MESSAGE_TIMEOUT_PET
                await asyncio.sleep(MESSAGE_TIMEOUT_PET)

            # Close the connection when we're done
            await connection.end_connection()

        tasks = [
            self.loop.create_task(go()),
            self.loop.create_task(connection.start_connection())
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertTrue(received_message)

    def test_can_connect(self):

        connection = self.CONNECTION_CLASS()

        async def go():
            CONNECTION_TIMEOUT_SECONDS = 5
            future = connection.await_until_connected()
            done, pending = await asyncio.wait(
                [future],
                timeout=CONNECTION_TIMEOUT_SECONDS,
                return_when=FIRST_COMPLETED
            )
            for f in pending:
                f.cancel()
            self.assertEqual(
                len(pending),
                0,
                "Connection did not complete within timeout"
            )
            self.assertTrue(done.pop().result())
            await connection.end_connection()

        tasks = [
            self.loop.create_task(go()),
            self.loop.create_task(connection.start_connection())
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))

class TestDiscordConnection(TestConnection, unittest.TestCase):
    CONNECTION_CLASS = DiscordConnection
    MESSAGE_CLASS = DiscordMessage
    CHANNEL_CLASS = DiscordChannel
