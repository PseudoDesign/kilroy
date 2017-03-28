import unittest
from kilroy.connections import DiscordConnection, DiscordMessage, DiscordChannel
import asyncio
from concurrent.futures import FIRST_COMPLETED


class ConnectionTestHandler:
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks = []

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def run_test(self, connection):
        self.tasks += [self.loop.create_task(connection.start_connection())]
        self.loop.run_until_complete(asyncio.wait(self.tasks))


class TestConnection:

    CONNECTION_CLASS = None
    MESSAGE_CLASS = None
    CHANNEL_CLASS = None
    TEST_CHANNEL_INFO = None

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
            self.CONNECTION_CLASS.get_channel_class(),
            self.CHANNEL_CLASS
            )

    def test_send_and_receive_message(self):
        MESSAGE = "Hello Discord"
        MESSAGE_TIMEOUT_SECONDS = 5
        MESSAGE_TIMEOUT_PET = .2
        self.received_message = False

        connection = self.CONNECTION_CLASS()

        async def message_listener(message):
            # Check if the test message came in
            if str(message) == MESSAGE and \
                  self.test_channel == message.get_channel():
                self.received_message = True

        async def go():
            await connection.await_until_connected()

            connection.add_message_listener(message_listener)
            self.test_channel = connection.get_channel_from_kwargs(
                **self.TEST_CHANNEL_INFO
                )
            await self.test_channel.send_text(connection, MESSAGE)

            # Spin until the message listener signals that we're done
            elapsed = 0
            while (not self.received_message) and \
                    (elapsed < MESSAGE_TIMEOUT_SECONDS):
                elapsed += MESSAGE_TIMEOUT_PET
                await asyncio.sleep(MESSAGE_TIMEOUT_PET)

            # Close the connection when we're done
            await connection.end_connection()

        tasks = [
            self.loop.create_task(go()),
            self.loop.create_task(connection.start_connection())
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertTrue(self.received_message)

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
