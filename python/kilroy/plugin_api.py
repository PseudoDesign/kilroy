class PluginApi:
    # A string with the name of this plugin
    PLUGIN_NAME = None
    # A list of PluginCommands handled by this plugin
    COMMANDS = []

    def __init__(self, name, **kwargs):
        """
        Any arguments added in the Kilroy config file will be passed on startup.
        :param name: REQUIRED: The name of this plugin
        :param kwargs:
        """
        if name != self.PLUGIN_NAME:
            raise AttributeError("Attempting to load an invalid plugin")
        self._command_dict = {}
        for c in self.COMMANDS:
            self._command_dict[c.COMMAND_NAME] = c

    def is_handled(self, message_str):
        """
        Determines if the message string is handled by this plugin
        :param message_str: The message to be checked with the kilry prefix stripped
        :type message_str: str
        :return: True if handled, else false
        """
        if message_str.split(" ")[0] == self.PLUGIN_NAME:
            return True
        return False

    async def message_handler(self, message, connection, db_connection):
        """
        Handles messages passed to this module.  By default, it will parse/call PluginCommands
        attached to this module.
        :param message: The message to be parsed, including the kilroy prefix
        :type message: Message
        :param connection: The connection that generated this message.
        :type connection: Connection
        :param db_connection:
        :type db_connection: kilroy.SqlConnection
        """
        command = str(message).split(" ")[1]
        if command in self._command_dict:
            await self._command_dict[command].execute_command(message, connection, db_connection)


class PluginCommand:
    # The name of this command
    COMMAND_NAME = None

    @classmethod
    async def execute_command(cls, message, connection, db_connection):
        raise NotImplementedError()


class TestCommand:
    COMMAND_NAME = "test_command"
    IS_CALLED = False

    @classmethod
    async def execute_command(cls, message, connection, db_connection):
        cls.IS_CALLED = True


class HelloKilroy(PluginApi):
    """
    An example plugin for Kilroy
    """
    PLUGIN_NAME = "hello_kilroy"

    def __init__(self, name, **kwargs):
        super().__init__(name, **kwargs)

    async def message_handler(self, message, connection, db_connection):
        pass


class TestPlugin(PluginApi):
    PLUGIN_NAME = "test_plugin"
    COMMANDS = [
        TestCommand
    ]

    def __init__(self, name):
        super().__init__(name)
        self.is_called = False

    async def message_handler(self, message, connection, db_connection):
        self.is_called = True
        await super().message_handler(message, connection, db_connection)
