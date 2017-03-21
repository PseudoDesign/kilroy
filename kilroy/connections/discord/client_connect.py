from .. import Connection
import discord
import asyncio
import yaml
import os


class DiscordConnection(discord.Client, Connection):

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

    async def start_connection(self):
        await self.start(self.__key)

    async def end_connection(self):
        await self.logout()
        await asyncio.sleep(.1)

    async def on_ready(self):
        await self._set_connection_state(True)
