import unittest
from kilroy.plugin_api import PluginApi


class TestPluginApi(unittest.TestCase):
    class PluginApiTester(PluginApi):
        pass

