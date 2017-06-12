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

    @classmethod
    async def execute_command(cls, message, connection, db_session):
        # Get the third argument, which (if exists) is the mention text of the user to query
        args = str(message).split(" ")
        if len(args) >= 3:
            c = message.get_channel()
            user = await c.find_user_by_mention_text(args[2])
        else:
            user = message.get_author()

        if user is not None:
            balance = await get_balance(db_session, user.get_db_obj(db_session))
            reply = "{} has a balance of {}₡".format(user.get_mention_text(), str(balance))
            await message.get_channel().send_text(connection, reply)


class SendCredits(PluginCommand):
    COMMAND_NAME = 'send'

    @classmethod
    async def execute_command(cls, message, connection, db_session):
        # Get the third argument, which (if exists) is the mention text of the user to query
        args = str(message).split(" ")
        recipient = None
        value = 0
        if len(args) >= 4:
            c = message.get_channel()
            recipient = await c.find_user_by_mention_text(args[2])
            try:
                value = int(args[3])
            except:
                value = -1

        if recipient is not None and value > 0:
            try:
                await send_credits(db_session,
                             message.get_author().get_db_obj(db_session),
                             recipient.get_db_obj(db_session),
                             value)
                reply = "Successfully sent {}₡ to {}"
            except ValueError:
                reply = "Unable to send {}₡ to {}"
            reply = reply.format(value, recipient.get_mention_text())
            await message.get_channel().send_text(connection, reply)


class KilroyPlugin(PluginApi):
    PLUGIN_NAME = plugin_name
    COMMANDS = [
        GetBalance,
        SendCredits
    ]
