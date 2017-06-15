from asyncio import Lock
from .ops import *
from kilroy.plugin_api import PluginApi, PluginCommand

__wallet_lock = Lock()

plugin_name = "wallet"

async def get_balance(db_session, db_user):
    """
    Returns the user's current credit balance.
    :param db_user: Get this user's credit balance
    :type db_user: kilroy.DbUser
    :param db_session:
    :return: BigInteger -- The user's credit balance
    """
    with await __wallet_lock:
        return ops.get_balance(db_session, db_user)


async def send_credits(db_session, source_db_user, destination_db_user, value):
    """
    Transfer credits from one user to another.  Raises ValueError if the operation can't be completed.
    :param db_session: The database session object to work on
    :param source_db_user: The party initiating the transaction
    :type source_db_user: kilroy.DbUser
    :param destination_db_user: The party receiving the transaction
    :type destination_db_user: kilroy.DbUser
    :param value: the number of credits to transfer
    """
    with await __wallet_lock:
        return ops.send_credits(db_session, source_db_user, destination_db_user, value)


class GetBalance(PluginCommand):
    COMMAND_NAME = 'balance'
    COMMAND_DESCRIPTION = "Query the balance of a user."
    COMMAND_ARGS = [
        ("user", "Optional.  Get this user's balance. Leave blank to get your own balance.")
    ]

    @classmethod
    async def execute_command(cls, message):
        # Get the third argument, which (if exists) is the mention text of the user to query
        args = message.plugin_command
        if len(args) >= 2:
            c = message.get_channel()
            user = await c.find_user_by_mention_text(args[1])
        else:
            user = message.author

        if user is not None:
            balance = await get_balance(message.db_session, user.get_db_obj(message.db_session))
            reply = "{} has a balance of {}₡".format(user.get_mention_text(), str(balance))
            await message.send_reply(reply)


class SendCredits(PluginCommand):
    COMMAND_NAME = 'send'
    COMMAND_DESCRIPTION = "Send credits to another user."
    COMMAND_ARGS = [
        ("recipient_user", "The user receiving your credits."),
        ("quantity", "The number of credits to send.")
    ]

    @classmethod
    async def execute_command(cls, message):
        # Get the third argument, which (if exists) is the mention text of the user to query
        args = message.plugin_command
        recipient = None
        value = 0
        if len(args) >= 3:
            c = message.channel
            recipient = await c.find_user_by_mention_text(args[1])
            try:
                value = int(args[2])
            except ValueError:
                value = -1

        if recipient is not None and value > 0:
            try:
                await send_credits(message.db_session,
                                   message.author.get_db_obj(message.db_session),
                                   recipient.get_db_obj(message.db_session),
                                   value)
                reply = "{} successfully sent {}₡ to {}"
            except ValueError:
                reply = "{}: Unable to send {}₡ to {}"
            reply = reply.format(message.author.get_mention_text(), value, recipient.get_mention_text())
            await message.send_reply(reply)


class KilroyPlugin(PluginApi):
    PLUGIN_NAME = plugin_name
    PLUGIN_DESCRIPTION = "A currency manager.  Allows users to send, receive, and store credits."
    COMMANDS = [
        GetBalance,
        SendCredits
    ]
