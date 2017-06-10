from .connections import *
from .conf import *
from .db import *
from .user import *
from .plugin_api import *
from .kilroy import *
import sys
from aioconsole import ainput


def run_with_console(*args):
    async def console():
        i = await ainput("Enter a command: ")
        print(i)
        await k.end_connections()

    if len(args) > 0:
        k = kilroy.Kilroy(args[0])
    else:
        k = kilroy.Kilroy()

    tasks = [
        k.loop.create_task(console()),
    ]
    k.start_connections(tasks)
    k.unload()



def main():
    COMMANDS = {
        "console": (run_with_console, "Start's a Kilroy connection with a console.  Accepts a config file."),
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
