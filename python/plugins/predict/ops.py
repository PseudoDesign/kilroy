from .db_objects import Market, BuyOrder, Transaction
from datetime import datetime
from . import YES_OPTION


def create_new_market(db_session, title, yes_option, no_option, expiration, facilitator_id):
    if expiration < datetime.now():
        raise ValueError()
    return Market.get_or_create(
        db_session,
        title=title,
        yes_option=yes_option,
        no_option=no_option,
        expiration=expiration,
        facilitator_id=facilitator_id
    )


def create_buy_order(db_session, market_id, option, price, expiration, user_id, quantity):
    if expiration < datetime.now() or price >= 100 or price <= 0:
        raise ValueError()
    b = BuyOrder(
        market_id=market_id,
        option=option,
        price=price,
        expiration=expiration,
        user_id=user_id,
        quantity=quantity
    )
    b.write_to_db(db_session)
    return b


def fill_buy_order(db_session, buy_order, quantity, user_id):
    if buy_order.remaining_quantity < quantity or buy_order.expiration <= datetime.now():
        raise ValueError()
    if buy_order.option == YES_OPTION:
        yes_holder = buy_order.user_id
        no_holder = user_id
    else:
        no_holder = buy_order.user_id
        yes_holder = user_id
    t = Transaction(
        yes_holder_id=yes_holder,
        no_holder_id=no_holder,
        buy_order_id=buy_order.id,
        quantity=quantity
    )
    t.write_to_db(db_session)
    return t
