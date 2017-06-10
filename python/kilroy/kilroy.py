from . import DiscordConnection, HelloKilroy, SqlConnection
import yaml
from threading import Lock
import asyncio


class Kilroy:
    DB_LOCATION = 'sqlite:///:memory:'

    __AVAILABLE_CONNECTIONS = [
        DiscordConnection,
    ]

    __AVAILABLE_PLUGINS = [
        HelloKilroy,
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
            command = str(message)[len(self.APP_PREFIX):]
            for p in self.plugins:
                if p.is_handled(command):
                    await p.message_handler(message, conn, self.db)

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

