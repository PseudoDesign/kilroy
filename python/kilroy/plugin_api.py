class PluginApi:
    # A string with the name of this plugin
    PLUGIN_NAME = None
    # A list of PluginCommands
    COMMANDS = None

    def __init__(self, name, **kwargs):
        """
        Any arguments added in the Kilroy config file will be passed on startup.
        :param name: REQUIRED: The name of this plugin
        :param kwargs:
        """
        if name != self.PLUGIN_NAME:
            raise AttributeError("Attempting to load an invalid plugin")

    def is_handled(self, message):
        """
        Determines if the message string is handled by this plugin
        :param message: The message to be checked
        :type message: str
        :return: True if handled, else false
        """
        return True


class PluginCommand:
    # The name of this command
    COMMAND_NAME = None


class HelloKilroy(PluginApi):
    """
    An example plugin for Kilroy
    """
    PLUGIN_NAME = "hello_kilroy"

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    async def command_handler(self, message, connection):
        pass


class TestPlugin(PluginApi):
    PLUGIN_NAME = "test_plugin"

    def __init__(self):
        self.is_called = False

    async def command_handler(self, message, connection):
        self.is_called = True
