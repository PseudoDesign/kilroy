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
    :param db_session:
    :param source_db_user:
    :type source_db_user: kilroy.DbUser
    :param destination_db_user:
    :type destination_db_user: kilroy.DbUser
    :param value: the number of credits to transfer
    """
    with await __wallet_lock:
        return ops.send_credits(db_session, source_db_user, destination_db_user, value)


class GetBalance(PluginCommand):
    COMMAND_NAME = 'balance'

    @classmethod
    async def execute_command(cls, message, connection, db_session):
        return await get_balance(db_session, message.get_author().get_db_obj())


class KilroyPlugin(PluginApi):
    PLUGIN_NAME = plugin_name
    COMMANDS = [
        GetBalance,
    ]
