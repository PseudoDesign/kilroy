import asyncio


class Connection:
    def __init__(self, **kwargs):
        self.__is_connected = False

    async def _set_connection_state(self, state):
        self.__is_connected = state

    def is_connected(self):
        return self.__is_connected

    async def await_until_connected(self):
        while not self.is_connected():
            await asyncio.sleep(.2)
        return True
