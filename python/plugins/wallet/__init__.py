from asyncio import Lock
from .ops import *

wallet_lock = Lock()

async def get_balance(db_session, db_user):
    """
    Returns the user's current credit balance.
    :param db_user: Get this user's credit balance
    :type db_user: kilroy.DbUser
    :param db_session:
    :return: BigInteger -- The user's credit balance
    """
    with await wallet_lock:
        return ops.get_balance(db_session, db_session)


async def send_credits(db_session, source_db_user, destination_db_user, value):
    """
    Transfer credits from one user to another.  Raises ValueError if the operation can't be completed.
    :param source_db_user:
    :type source_db_user: kilroy.DbUser
    :param destination_db_user:
    :type destination_db_user: kilroy.DbUser
    :param value: the number of credits to transfer
    """
    with await wallet_lock:
        return ops.send_credits(db_session, source_db_user, destination_db_user, value)

