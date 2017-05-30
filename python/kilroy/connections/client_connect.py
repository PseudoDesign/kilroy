import asyncio

from kilroy.conf import ConfigEntry


class Channel:
    async def send_text(self, channel, text):
        raise NotImplementedError()

    def get_id(self):
        """
        Return the client-unique ID of this channel
        :return: str
        """
        raise NotImplementedError()

    async def get_users(self):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.get_id() == other.get_id()

    def __ne__(self, other):
        return self.get_id() != other.get_id()


class Message:
    def get_channel(self):
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


class Connection(ConfigEntry):
    MESSAGE_CLASS = Message
    CHANNEL_CLASS = Channel
    CONFIG_ENTRY_NAME = None
    CLIENT_NAME = None

    def __init__(self, **kwargs):
        self.__is_connected = False
        self.__message_listeners = []

    @classmethod
    async def send_message(cls, message, **channel_kwargs):
        await cls.get_channel(channel_kwargs).send_message(message)

    @classmethod
    def get_message_class(cls):
        return cls.MESSAGE_CLASS

    @classmethod
    def get_channel_class(cls):
        return cls.CHANNEL_CLASS

    def get_channel_from_kwargs(self, **channel_kwargs):
        return self.get_channel_class().from_kwargs(self, **channel_kwargs)

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

    def get_user_info(self):
        raise NotImplementedError()

    def add_message_listener(self, listener):
        if listener not in self.__message_listeners:
            self.__message_listeners += [listener]
