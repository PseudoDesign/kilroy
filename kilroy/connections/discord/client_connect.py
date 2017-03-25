from .. import Connection, Message, Channel
import discord
import asyncio
import yaml
import os


class DiscordChannel(Channel):
    def __init__(self, connection, **kwargs):
        '''
            kwargs:
                channel_id - indicates a private channel or server channel
                user_id - indicates a DM
        '''
        self.__channel = None
        self.__is_dm = False
        print("ici")
        if "channel_id" in kwargs:
            self.__channel = connection.get_channel(kwargs["channel_id"])
        elif "user_id" in kwargs:
            self.__channel = connection.get_user_info(kwargs["user_id"])
            self.__is_dm = True
        else:
            raise ValueError()

        self.__connection = connection

    async def send_message(self, message):
        await self.__connection.send_message(self.__channel, message)

class DiscordMessage(Message):
    pass


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
