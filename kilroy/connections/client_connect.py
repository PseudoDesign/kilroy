import asyncio
from threading import Lock


class Connection:
    def __init__(self, **kwargs):
        self.__is_connected = False
        self.__connection_lock = Lock()

    def __set_connection_state(self, state):
        with self.__connection_lock:
            self.__is_connected = state

    def is_connected(self):
        return self.__is_connected

    async def await_until_connected(self):
        while not self.is_connected():
            await asyncio.sleep(.1)
        return self.is_connected()
