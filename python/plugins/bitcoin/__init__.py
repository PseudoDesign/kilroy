from kilroy.plugin_api import PluginApi, PluginCommand
import requests

plugin_name = "bitcoin"


def fetch_price():
    url = 'https://blockchain.info/ticker'
    response = requests.get(url).json()
    return response


class GetPrice(PluginCommand):
    COMMAND_NAME = 'price'
    COMMAND_DESCRIPTION = "Query the price of Bitcoin."
    COMMAND_ARGS = [
        ("user", "Optional.  Get this user's balance. Leave blank to get your own balance.")
    ]

    @classmethod
    async def execute_command(cls, message):
        # Set a reply with the current price of Bitcoin
        reply = fetch_price()
        usd = reply['USD']
        await message.send_reply(str(usd))


class KilroyPlugin(PluginApi):
    PLUGIN_NAME = plugin_name
    PLUGIN_DESCRIPTION = "Fetch the current price of bitcoin."
    COMMANDS = [
        GetPrice,
    ]


