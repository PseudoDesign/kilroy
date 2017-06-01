from . import *
import yaml
from threading import Lock


class Kilroy:

    __AVAILABLE_CONNECTIONS = [
        DiscordConnection,
    ]

    __AVAILABLE_PLUGINS = [
        HelloKilroy,
    ]

    def __init__(self, conf_file=None):
        """
        A chatbot plugin API for multiple chat services.
        :param conf_file: File path of a config .yaml file
        """
        self.__plugin_lock = Lock()
        self.available_connections = {}
        for a in self.__AVAILABLE_CONNECTIONS:
            self.available_connections[a.CLIENT_NAME] = a
        self.available_plugins = {}
        for a in self.__AVAILABLE_PLUGINS:
            self.available_plugins[a.PLUGIN_NAME] = a
        self.connections = []
        self.plugins = []
        if conf_file is not None:
            fpt = open(conf_file, 'r')
            data = yaml.load(fpt)
            fpt.close()

            for c in data['connections']:
                conn = self.available_connections[c['client']](**c)
                conn.add_message_listener(self.message_handler)
                self.connections += [conn]

            for p in data['plugins']:
                self.load_plugin(self.available_plugins[p['name']](**p))

    def message_handler(self, message, conn):
        pass

    def load_plugin(self, plugin):
        """
        :param plugin: A plugin class to install.
        :type plugin: PluginApi
        :return:
        """
        with self.__plugin_lock:
            if plugin in self.plugins:
                return None
            self.plugins += [plugin]

