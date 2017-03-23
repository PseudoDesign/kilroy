import asyncio


class Channel:
    pass


class Message:
    pass


class Connection:
    MESSAGE_CLASS = Message
    CHANNEL_CLASS = Channel

    def __init__(self, **kwargs):
        self.__is_connected = False
        self.__message_listeners = []

    @classmethod
    def get_message_class(cls):
        return cls.MESSAGE_CLASS

    @classmethod
    def get_channel_class(cls):
        return cls.CHANNEL_CLASS

    async def _set_connection_state(self, state):
        self.__is_connected = state

    def is_connected(self):
        return self.__is_connected

    async def await_until_connected(self):
        while not self.is_connected():
            await asyncio.sleep(.2)
        return True

    async def _message_handler(self, message):
        for listener in self.__message_listeners:
            await listener(message)

    async def send_message_text(self, message_text):
        raise NotImplementedError()

    async def start_connection(self):
        raise NotImplementedError()

    def end_connection(self):
        raise NotImplementedError()

    def add_message_listener(self, listener):
        if listener not in self.__message_listeners:
            self.__message_listeners += [listener]
