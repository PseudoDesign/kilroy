from .connections import *
from .conf import *
from .db import *
from .user import *
from .plugin_api import *
import sys
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
                self.connections += [self.available_connections[c['client']](**c)]

            for p in data['plugins']:
                self.load_plugin(self.available_plugins[p['name']](**p))

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


def main():
    COMMANDS = {
    #    "make_config": (create_sample_config_file, "Create a sample config file."),
    }
    if len(sys.argv) <= 1:
        print("Hello, kilroy")
    else:
        command = sys.argv[1]
        if command in COMMANDS:
            COMMANDS[command][0](*sys.argv[2:])
        else:
            print("Commands:")
            for command in COMMANDS:
                print(command + " - " + COMMANDS[command][1])