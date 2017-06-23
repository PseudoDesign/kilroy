import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from tests.test_db import TestDbConnection
from plugins.predict.ops import create_new_market, create_buy_order
from plugins.predict.db_objects import Market, BuyOrder
from plugins.predict import YES_OPTION, NO_OPTION


class TestPredictOps(TestDbConnection, unittest.TestCase):
    TITLE = "Is this a test market?"
    YES_OPTION = "This is a test market"
    NO_OPTION = "This is not a test market"
    EXPIRATION = datetime.now() + timedelta(days=1)
    FACILITATOR_ID = 1

    def setUp(self):
        super().setUp()
        self.test_market = create_new_market(
            self._connection.session,
            title=self.TITLE,
            yes_option=self.YES_OPTION,
            no_option=self.NO_OPTION,
            expiration=self.EXPIRATION,
            facilitator_id=self.FACILITATOR_ID
        )
        self.test_buy_order = create_buy_order(
            self._connection.session,
            market_id=self.test_market.id,
            option=YES_OPTION,
            price=75,
            expiration=datetime.now() + timedelta(minutes=5),
            user_id=self.FACILITATOR_ID
        )

    def test_create_market(self):
        m = Market.get_from_db_by_kwargs(self._connection.session, title=self.TITLE)
        self.assertEqual(m.yes_option, self.YES_OPTION)
        self.assertEqual(m.no_option, self.NO_OPTION)
        self.assertEqual(m.expiration, self.EXPIRATION)
        self.assertEqual(m.facilitator_id, self.FACILITATOR_ID)

    def test_create_buy_order(self):
        b = BuyOrder.get_from_db_by_kwargs(self._connection.session, user_id=self.FACILITATOR_ID)
        self.assertEqual(b.market_id, self.test_market.id)
        self.assertEqual(b.option, YES_OPTION)
        self.assertEqual(b.price, 75)
        self.assertEqual(b.user_id, self.FACILITATOR_ID)

    def test_fill_buy_order(self):
        pass

    def test_query_open_orders(self):
        pass


class TestPluginApi:
    pass
