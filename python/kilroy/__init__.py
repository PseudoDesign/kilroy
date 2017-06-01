from .connections import *
from .conf import *
from .db import *
from .user import *
from .plugin_api import *
from .kilroy import *
import sys



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