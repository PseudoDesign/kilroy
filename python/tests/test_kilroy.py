import unittest
import os
from kilroy import Kilroy


class TestKilroy(unittest.TestCase):
    CONFIG_FILE = KEY_FILE_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".test_kilroy_config.yaml"
        )

    def test_create_from_config(self):
        TESTED_CONNECTIONS = [
            "discord"
        ]
        TESTED_PLUGINS = [
            "test_plugin"
        ]

        k = Kilroy(self.CONFIG_FILE)
        self.assertEqual(len(TESTED_CONNECTIONS), len(k.connections))
        self.assertEqual(len(TESTED_PLUGINS), len(k.plugins))
        for c in TESTED_CONNECTIONS:
            self.assertIn(c, k.connections)
        for p in TESTED_PLUGINS:
            self.assertIn(p, k.plugins)


