import unittest
from datetime import datetime, timedelta
from tests.test_db import TestDbConnection
from plugins.predict.ops import create_new_market, create_buy_order, fill_buy_order
from plugins.predict.db_objects import Market, BuyOrder, Transaction
from plugins.predict import YES_OPTION


class TestPredictOps(TestDbConnection, unittest.TestCase):
    TITLE = "Is this a test market?"
    YES_OPTION = "This is a test market"
    NO_OPTION = "This is not a test market"
    EXPIRATION = datetime.now() + timedelta(days=1)
    FACILITATOR_ID = 1
    PURCHASER_ID = 2

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
            user_id=self.FACILITATOR_ID,
            quantity=50
        )

    def test_create_market(self):
        m = Market.get_from_db_by_kwargs(self._connection.session, title=self.TITLE)
        self.assertEqual(m.yes_option, self.YES_OPTION)
        self.assertEqual(m.no_option, self.NO_OPTION)
        self.assertEqual(m.expiration, self.EXPIRATION)
        self.assertEqual(m.facilitator_id, self.FACILITATOR_ID)

    def test_create_buy_order(self):
        with self.assertRaises(ValueError):
            create_buy_order(
                self._connection.session,
                market_id=self.test_market.id,
                option=YES_OPTION,
                price=102,
                expiration=datetime.now() + timedelta(minutes=5),
                user_id=self.FACILITATOR_ID,
                quantity=50
            )
        with self.assertRaises(ValueError):
            create_buy_order(
                self._connection.session,
                market_id=self.test_market.id,
                option=YES_OPTION,
                price=14,
                expiration=datetime.now() + timedelta(minutes=-5),
                user_id=self.FACILITATOR_ID,
                quantity=50
            )
        b = BuyOrder.get_from_db_by_kwargs(self._connection.session, user_id=self.FACILITATOR_ID)
        self.assertEqual(b.market_id, self.test_market.id)
        self.assertEqual(b.option, YES_OPTION)
        self.assertEqual(b.price, 75)
        self.assertEqual(b.user_id, self.FACILITATOR_ID)
        self.assertEqual(b.filled_quantity, 0)

    def test_fill_buy_order(self):
        # with self.assertRaises(ValueError):
        #    pass
        fill_buy_order(
            self._connection.session,
            buy_order=self.test_buy_order,
            quantity=25,
            user_id=self.PURCHASER_ID,
        )
        t = Transaction.get_from_db_by_kwargs(
            self._connection.session,
            yes_holder_id=self.FACILITATOR_ID,
            no_holder_id=self.PURCHASER_ID
        )
        self.assertEqual(t.quantity, 25)
        self.assertEqual(t.buy_order_id, self.test_buy_order.id)


class TestPluginApi:
    pass
