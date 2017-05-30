from .connections import *
from .conf import *
from .db import *
from .user import *
from .plugin_api import *
import sys
import yaml


class Kilroy:

    AVAILABLE_CONNECTIONS = [
        DiscordConnection,
    ]

    def __init__(self, conf_file=None):
        """
        A chatbot plugin API for multiple chat services.
        :param conf_file: File path of a config .yaml file
        """
        available_connections = {}
        for a in self.AVAILABLE_CONNECTIONS:
            available_connections[a.CLIENT_NAME] = a
        fpt = open(conf_file, 'r')
        data = yaml.load(fpt)
        fpt.close()
        for c in data['connections']:
            available_connections[c.]


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