from unittest import TestCase
from unittest.mock import patch, MagicMock
from plugins.bitcoin import fetch_price


class TestBitcoin(TestCase):
    def test_fetch_price_returns_USD(self):
        expected_key = "USD"
        # last transaction price, currency symbol, bid, ask
        expected_subkeys = ['last', 'symbol', 'buy', 'sell']
        resp = fetch_price()
        self.assertIn(expected_key, resp)
        for e in expected_subkeys:
            self.assertIn(e, resp[expected_key])


