import unittest
from connections import Connection, CLIENT_DISCORD
import asyncio


class TestDiscordConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.connection = Connection(client=CLIENT_DISCORD)

    def test_can_connect(self):
        CONNECTION_TIMEOUT_SECONDS = 5
