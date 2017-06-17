import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta
from tests.test_db import TestDbConnection
from plugins.predict.ops import create_new_market
from plugins.predict.db_objects import Market


class TestPredict(TestDbConnection, unittest.TestCase):
    TITLE = "Is this a test market?"
    YES_OPTION = "This is a test market"
    NO_OPTION = "This is not a test market"
    EXPIRATION = datetime.now() + timedelta(days=1)
    FACILITATOR_ID = 1

    @classmethod
    def setUpClass(cls):
        pass

    def test_create_market(self):
        create_new_market(
            self._connection.session,
            title=self.TITLE,
            yes_option=self.YES_OPTION,
            no_option=self.NO_OPTION,
            expiration=self.EXPIRATION,
            facilitator_id=self.FACILITATOR_ID
        )
        m = Market.get_from_db_by_kwargs(self._connection.session, title=self.TITLE)
        self.assertEqual(m.yes_option, self.YES_OPTION)
        self.assertEqual(m.no_option, self.NO_OPTION)
        self.assertEqual(m.expiration, self.EXPIRATION)
        self.assertEqual(m.facilitator_id, self.FACILITATOR_ID)


    def test_create_buy_order(self):
        pass

    def test_fill_buy_order(self):
        pass

    def test_query_open_orders(self):
        pass

    def test_wallet_access(self):
        pass


class TestPluginApi:
    pass
