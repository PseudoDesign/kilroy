from .db_objects import Market


def create_new_market(db_session, title, yes_option, no_option, expiration, facilitator_id):
    m = Market.get_from_db_by_kwargs(
        db_session,
        title=title,
        yes_option=yes_option,
        no_option=no_option,
        expiration=expiration,
        facilitator_id=facilitator_id
    )
    if m is None:
        Market(
            title=title,
            yes_option=yes_option,
            no_option=no_option,
            expiration=expiration,
            facilitator_id=facilitator_id,
        ).write_to_db(db_session)

