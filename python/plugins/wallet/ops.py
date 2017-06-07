from .db_objects import *


def _get_or_create_balance(db_session, db_user):
    bal = UserBalance.get_from_db_by_kwargs(db_session, user_id=db_user.id)
    if bal is None:
        bal = UserBalance(user_id=db_user.id)
        bal.write_to_db(db_session)
    return bal


def set_balance(db_session, db_user, value):
    """
    Set's the user's balance to value
    :param db_user: Get this user's credit balance
    :type db_user: kilroy.DbUser
    :param db_session:
    :param value: The number of credits in this wallet
    :type value: BigInteger
    """
    bal = _get_or_create_balance(db_session, db_user)
    bal.balance = value
    bal.write_to_db(db_session)


def send_credits(db_session, source_db_user, destination_db_user, value):
    """
    Transfer credits from one user to another.  Raises ValueError if the operation can't be completed.
    :param source_db_user:
    :type source_db_user: kilroy.DbUser
    :param destination_db_user:
    :type destination_db_user: kilroy.DbUser
    :param value: the number of credits to transfer
    """
    s = _get_or_create_balance(db_session, source_db_user)
    d = _get_or_create_balance(db_session, destination_db_user)
    if s.balance - value < 0:
        raise ValueError("Source user does not have enough credits")
    set_balance(db_session, source_db_user, s.balance - value)
    set_balance(db_session, destination_db_user, d.balance + value)


def get_balance(db_session, db_user):
    return _get_or_create_balance(db_session, db_user).balance
