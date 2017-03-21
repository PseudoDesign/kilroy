from .. import Connection
import discord
from threading import Thread, Lock


class DiscordConnection(Connection):

    __client = discord.Client()

    def __init__(self, **kwargs):
        super().__init__()
        self.__run_thread = Thread(target=self.run)
        self.__run_lock = Lock()
        self.__is_thread_running = False

    def run(self):
        self.__client.run('key')

    def start_connection(self):
        with self.__run_lock:
            if not self.__is_thread_running:
                self.__is_thread_running = True
                self.__run_thread.start()

    @__client.event
    async def on_ready(self):
        self.__set_connection_state(True)
