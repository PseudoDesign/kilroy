import unittest

import yaml

from python.kilroy import ConfigEntry, Config


class TestConfig(unittest.TestCase):

    EXAMPLE_CONFIG_STRING = \
        "MODULE_NAME:\n  example_data_1: sample\n"

    def test_get_example_config_string(self):
        self.assertEqual(
            ConfigEntry.get_example_config_string(comment=True),
            "# MODULE_NAME:\n#   example_data_1: sample\n"
        )
        self.assertEqual(
            ConfigEntry.get_example_config_string(),
            self.EXAMPLE_CONFIG_STRING
        )

    def test_create_dict(self):
        Config.add_entry(ConfigEntry)
        data = yaml.load(self.EXAMPLE_CONFIG_STRING)
        entry = Config.create_entry(ConfigEntry.CONFIG_ENTRY_NAME, data)
        self.assertIs(
            type(entry),
            ConfigEntry
        )
