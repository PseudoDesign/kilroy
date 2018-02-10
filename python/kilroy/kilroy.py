from . import DiscordConnection, HelloKilroy, SqlConnection
import yaml
from threading import Lock
import asyncio

from plugins.wallet import KilroyPlugin as Wallet

from plugins.bitcoin import KilroyPlugin as Bitcoin


class PluginMessage:
    def __init__(self, message, connection, db_session):
        """
        A set of helper functions for handling a kilroy message
        :param message: the client-specific message
        :param connection: the connection that generated this message
        :param db_session: the database session used by plugins
        """
        self.message = message
        self.channel = message.get_channel()
        self.connection = connection
        self.db_session = db_session
        self.author = message.get_author()

    async def send_reply(self, text):
        """
        Sends a reply to the channel that generated this message
        :param text: The text to send
        """
        await self.channel.send_text(self.connection, text)

    @property
    def args(self):
        """
        A list of the parameters that make up this message.
        """
        args = []
        for s in str(self.message).split(" "):
            if len(s) > 0:
                args += [s]
        return args

    @property
    def plugin_prefix(self):
        """
        The application and plugin prefix, i.e. args[0]
        """
        return self.args[0]

    @property
    def plugin_command(self):
        """
        A list containing command passed to the plugin and the additional arguments
        """
        return self.args[1:]

    def __str__(self):
        return str(self.message)


class Kilroy:
    DB_LOCATION = 'sqlite:///:memory:'

    __AVAILABLE_CONNECTIONS = [
        DiscordConnection,
    ]

    __AVAILABLE_PLUGINS = [
        HelloKilroy,
        Wallet,
        Bitcoin
    ]

    APP_PREFIX = "!k."

    def __init__(self, conf_file=None):
        """
        A chatbot plugin API for multiple chat services.
        :param conf_file: File path of a config .yaml file
        """
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.__plugin_lock = Lock()
        self.available_connections = {}
        for a in self.__AVAILABLE_CONNECTIONS:
            self.available_connections[a.CLIENT_NAME] = a
        self.available_plugins = {}
        for a in self.__AVAILABLE_PLUGINS:
            self.available_plugins[a.PLUGIN_NAME] = a

        self.connections = []
        self.plugins = []
        self.db = None

        if conf_file is not None:
            fpt = open(conf_file, 'r')
            data = yaml.load(fpt)
            fpt.close()

            if 'sql_connection' in data:
                db_info = data['sql_connection']
                self.db = SqlConnection(db_info)
                self.db.create_tables()
                self.db.start_connection()

            for c in data['connections']:
                conn = self.available_connections[c['client']](**c)
                conn.add_message_listener(self._message_handler)
                self.connections += [conn]

            for p in data['plugins']:
                self.load_plugin(self.available_plugins[p['name']](**p))

        if self.db is None:
            self.db = SqlConnection(self.DB_LOCATION)
            self.db.create_tables()
            self.db.start_connection()

    async def _message_handler(self, message, conn):
        if str(message).startswith(self.APP_PREFIX):
            print("Message: " + str(message))
            command = str(message)[len(self.APP_PREFIX):]
            for p in self.plugins:
                plugin_message = PluginMessage(message, conn, self.db.session)
                if p.is_handled(plugin_message):
                    await p.message_handler(plugin_message)

    def start_connections(self, additional_tasks=[]):
        tasks = additional_tasks
        for c in self.connections:
            tasks += [self.loop.create_task(c.start_connection())]
        self.loop.run_until_complete(asyncio.wait(tasks))

    async def end_connections(self):
        for c in self.connections:
            await c.end_connection()

    def unload(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def load_plugin(self, plugin):
        """
        :param plugin: A plugin to install.
        :type plugin: PluginApi object
        :return:
        """
        with self.__plugin_lock:
            if plugin in self.plugins:
                return None
            self.plugins += [plugin]

