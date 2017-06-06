from .db_objects import *


def _get_or_create_balance(db_user, db_session):
    bal = UserBalance.get_from_db_by_kwargs(db_session, user_id=db_user.id)
    if bal is None:
        bal = UserBalance(user_id=db_user.id)
        bal.write_to_db(db_session)
    return bal


def get_balance(db_user, db_session):
    """
    Returns the user's current credit balance.
    :param db_user: Get this user's credit balance
    :type db_user: kilroy.DbUser
    :param db_session:
    :return: BigInteger -- The user's credit balance
    """
    bal = _get_or_create_balance(db_user, db_session)
    return bal.balance


def set_balance(db_user, db_session, value):
    """
    Set's the user's balance to value
    :param db_user: Get this user's credit balance
    :type db_user: kilroy.DbUser
    :param db_session:
    :return: Float -- The user's credit balance
    :param value: The number of credits in this wallet
    :type value: BigInteger
    """
    bal = _get_or_create_balance(db_user, db_session)
    bal.balance = value
    bal.write_to_db(db_session)
