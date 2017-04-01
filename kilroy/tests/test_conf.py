import unittest
from kilroy.conf import ConfigEntry
import yaml


class TestConfig(unittest.TestCase):
    def test_get_example_config_string(self):
        self.assertEqual(
            ConfigEntry.get_example_config_string(True),
            "# entry_type:\n#   example_data_1: sample\n#   name: MODULE_NAME\n"
        )
        self.assertEqual(
            ConfigEntry.get_example_config_string(),
            "entry_type:\n  example_data_1: sample\n  name: MODULE_NAME\n"
        )
