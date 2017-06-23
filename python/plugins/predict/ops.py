from .db_objects import Market, BuyOrder
from datetime import datetime


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


def create_buy_order(db_session, market_id, option, price, expiration, user_id):
    if expiration < datetime.now() or price >= 100 or price <= 0:
        raise ValueError()
    return BuyOrder.get_or_create(
        db_session,
        market_id=market_id,
        option=option,
        price=price,
        expiration=expiration,
        user_id=user_id
    )
