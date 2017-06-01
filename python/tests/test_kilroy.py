import unittest
import os
from kilroy import Kilroy
import asyncio
from kilroy import DiscordConnection, HelloKilroy


class TestKilroy(unittest.TestCase):
    CONFIG_FILE = KEY_FILE_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".test_kilroy_config.yaml"
        )

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_create_from_config(self):
        TESTED_CONNECTION = DiscordConnection
        TESTED_PLUGIN = HelloKilroy

        k = Kilroy(self.CONFIG_FILE)
        self.assertIs(TESTED_CONNECTION, k.connections[0].__class__)
        self.assertIs(TESTED_PLUGIN, k.plugins[0].__class__)
