import unittest
from kilroy.conf import ConfigEntry, Config
import yaml


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

    def test_create_from_yaml(self):
        Config.add_entry(ConfigEntry)
        entry = Config.create_entry_from_yaml(self.EXAMPLE_CONFIG_STRING)
        self.assertIs(
            type(entry),
            ConfigEntry
        )
