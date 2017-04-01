import unittest
from kilroy.conf import ConfigEntry, Config
import yaml


class TestConfig(unittest.TestCase):

    EXAMPLE_CONFIG_STRING = \
        "entry_type:\n  example_data_1: sample\n  name: MODULE_NAME\n"

    def test_get_example_config_string(self):
        self.assertEqual(
            ConfigEntry.get_example_config_string(comment=True),
            "# entry_type:\n#   example_data_1: sample\n#   name: MODULE_NAME\n"
        )
        self.assertEqual(
            ConfigEntry.get_example_config_string(),
            self.EXAMPLE_CONFIG_STRING
        )

    def test_create_from_yaml(self):
        Config.add_config_entry(ConfigEntry)
        entry = Config.create_from_yaml(self.EXAMPLE_CONFIG_STRING)
        self.assertEqual(
            type(entry),
            ConfigEntry
        )
