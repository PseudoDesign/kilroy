import unittest
from kilroy import DiscordConnection
import asyncio
from concurrent.futures import FIRST_COMPLETED


class TestDiscordConnection(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.connection = DiscordConnection()

    def test_send_and_receive_message(self):
        MESSAGE = "Hello Discord"
        MESSAGE_TIMEOUT_SECONDS = 5
        received_message = False

        async def message_listener(message):
            # Check if the test message came in
            if message.text == MESSAGE:
                received_message = True

        async def go():
            await self.connection.await_until_connected()
            self.connection.add_message_listener(message_listener)
            await self.connection.send_message_text(MESSAGE)

            # Spin until the message listener signals that we're done
            while not received_message:
                await asyncio.sleep(.2)

            # Close the connection when we're done
            await self.connection.end_connection()

        futures = [
            self.loop.create_task(go()),
            self.loop.create_task(self.connection.start_connection())
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))
        self.assertTrue(received_message)

    def test_can_connect(self):
        async def go():
            CONNECTION_TIMEOUT_SECONDS = 5
            future = self.connection.await_until_connected()
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
            await self.connection.end_connection()

        tasks = [
            self.loop.create_task(go()),
            self.loop.create_task(self.connection.start_connection())
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))
