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
        args = message.plugin_command

        currency = 'USD'
        reply = fetch_price()
        if len(args) >= 2:
            if args[1] in reply:
                currency = args[1]
            else:
                await message.send_reply("Currency {0} is not supported".format(args[1]))
                return
        response = "```\n" \
                   "Bitcoin Price in {0}:" \
                   "\n\n" \
                   "Last: {1} {2}\n" \
                   "Bid: {1} {3}\n" \
                   "Ask: {1} {4}\n" \
                   "```"
        reply = reply[currency]
        response = response.format(currency, reply['symbol'], reply['last'], reply['buy'], reply['sell'])
        await message.send_reply(response)



class KilroyPlugin(PluginApi):
    PLUGIN_NAME = plugin_name
    PLUGIN_DESCRIPTION = "Fetch the current price of bitcoin."
    COMMANDS = [
        GetPrice,
    ]


