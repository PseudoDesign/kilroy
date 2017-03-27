from .. import Connection, Message, Channel
import discord
import asyncio
import yaml
import os


class DiscordChannel(Channel):

    def __init__(self, discord_channel):
        self.__channel = discord_channel

    @staticmethod
    def from_kwargs(connection, **kwargs):
        '''
            kwargs:
                channel_id - indicates a private channel or server channel
                user_id - indicates a DM
        '''
        server = None
        if "server_id" in kwargs:
            server = connection.get_server(str(kwargs["server_id"]))
        if "channel_id" in kwargs:
            if server is not None:
                t = server
            else:
                t = connection
            channel = t.get_channel(str(kwargs["channel_id"]))
        elif "user_id" in kwargs:
            channel = connection.get_user_info(kwargs["user_id"])
        else:
            raise ValueError()

        return DiscordChannel(channel)

    def get_id(self):
        return self.__channel.id

    async def send_text(self, connection, text):
        await connection.send_message(self.__channel, text)

class DiscordMessage(Message):
    def __init__(self, message):
        self.__discord_message = message

    def __str__(self):
        return self.__discord_message.content

    def get_channel(self):
        return DiscordChannel(self.__discord_message.channel)


class DiscordConnection(discord.Client, Connection):
    MESSAGE_CLASS = DiscordMessage
    CHANNEL_CLASS = DiscordChannel

    KEY_FILE_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        ".keys.yaml"
        )

    def __init__(self):
        fpt = open(self.KEY_FILE_LOCATION, 'r')
        keys = yaml.load(fpt)
        fpt.close()
        self.__key = keys['client_oauth_token']
        discord.Client.__init__(self)
        Connection.__init__(self)

    async def send_message_text(self, message_text):
        await asyncio.sleep(.1)

    async def start_connection(self):
        await self.start(self.__key)

    async def end_connection(self):
        await self.close()
        await self._set_connection_state(False)
        await asyncio.sleep(.5)

    async def on_ready(self):
        await self._set_connection_state(True)

    async def on_message(self, message):
        my_message = DiscordMessage(message)
        await self._message_handler(my_message)