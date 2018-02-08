from .connections import *
from .conf import *
from .db import *
from .user import *
from .plugin_api import *
from .kilroy import *
from .strings import *
import sys
from aioconsole import ainput


def run_with_console(*args):
    async def console():
        i = ""
        if "-q" not in args:
            print(strings.CONSOLE_LICENSE_NOTICE)
        while i != "quit":
            i = await ainput("Enter a command: ")
            i = i.lower()
            if i in commands:
                if commands[i] is not None:
                    await commands[i]()
            else:
                print("'" + i + "' " + "is not a valid command.")
        print("Shutting down...")
        await k.end_connections()

    conf_file = None
    for a in args:
        if not a.startswith("-"):
            conf_file = a
            break

    k = kilroy.Kilroy(conf_file)

    commands = {
        "quit": None
    }

    tasks = [
        k.loop.create_task(console()),
    ]
    k.start_connections(tasks)
    k.unload()


def print_commands(commands, *args):
    print("Commands:")
    for command in commands:
        print(command + " - " + commands[command][1])


def main():
    COMMANDS = {
        "console": (run_with_console, "Start's a Kilroy connection with a console.  Accepts a config file."),
    }

    if len(sys.argv) <= 1:
        print_commands(COMMANDS)
    else:
        command = sys.argv[1]
        if command in COMMANDS:
            COMMANDS[command][0](*sys.argv[2:])
        else:
            print_commands(COMMANDS)
