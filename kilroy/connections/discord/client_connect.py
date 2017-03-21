from .. import Connection
import discord
import asyncio


class DiscordConnection(discord.Client, Connection):

    def __init__(self):
        discord.Client.__init__(self)
        Connection.__init__(self)

    async def start_connection(self):
        await self.start('key')
