import unittest
import os
from kilroy import Kilroy
import asyncio
from kilroy import DiscordConnection, HelloKilroy, TestPlugin


class TestKilroy(unittest.TestCase):
    CONFIG_FILE = KEY_FILE_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".test_kilroy_config.yaml"
        )

    TESTED_CONNECTION = DiscordConnection
    TESTED_PLUGIN = HelloKilroy

    # def test_create_from_config(self):
    #    k = Kilroy(self.CONFIG_FILE)
    #    self.assertIs(self.TESTED_CONNECTION, k.connections[0].__class__)
    #    self.assertIs(self.TESTED_PLUGIN, k.plugins[0].__class__)
    #    k.unload()

    def test_load_plugin(self):

        async def go():
            await k.connections[0].await_until_connected()
            test_channel = k.connections[0].get_channel_from_kwargs(server_id=410949404590080000,
                                                                    channel_id=410949404590080002)
            await test_channel.send_text(k.connections[0], "!k.test_plugin herp derp")
            await asyncio.sleep(3)
            await k.end_connections()

        k = Kilroy(self.CONFIG_FILE)
        t = TestPlugin("test_plugin")
        k.load_plugin(t)
        tasks = [
            k.loop.create_task(go()),
        ]
        k.start_connections(tasks)
        self.assertTrue(t.is_called)
        k.unload()

    def test_plugin_command(self):
        TEST_COMMAND_NAME = "test_command"

        async def go():
            await k.connections[0].await_until_connected()
            test_channel = k.connections[0].get_channel_from_kwargs(server_id=410949404590080000,
                                                                    channel_id=410949404590080002)
            await test_channel.send_text(k.connections[0], "!k.test_plugin test_command derp")
            await asyncio.sleep(3)
            await k.end_connections()

        k = Kilroy(self.CONFIG_FILE)
        t = TestPlugin("test_plugin")
        k.load_plugin(t)
        tasks = [
            k.loop.create_task(go()),
        ]
        k.start_connections(tasks)
        self.assertTrue(t._command_dict[TEST_COMMAND_NAME].IS_CALLED)
        k.unload()
