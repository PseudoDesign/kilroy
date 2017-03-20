import unittest
from kilroy import DiscordConnection
import asyncio
from concurrent.futures import FIRST_COMPLETED


class TestDiscordConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = DiscordConnection()
        cls.connection.start_connection()

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
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(go())
        loop.close()
