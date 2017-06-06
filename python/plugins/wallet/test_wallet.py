import unittest
from plugins import wallet
from kilroy.db.user import DbUser
from tests.test_db import TestDbConnection


class TestWallet(TestDbConnection, unittest.TestCase):
    TEST_USER_ID = 2
    TEST_USER_ID_2 = 5

    def test_get_and_set_balance(self):
        # Should be 0 by default since the user didn't exist before now
        user = DbUser(id=self.TEST_USER_ID)
        balance = wallet.get_balance(user, self._connection.session)
        self.assertEqual(0, balance)
        user = DbUser(id=self.TEST_USER_ID_2)
        wallet._set_balance(user, self._connection.session, 5)
        balance = wallet.get_balance(user, self._connection.session)
        self.assertEqual(5, balance)

    def test_transactions(self):
        user_1 = DbUser(id=self.TEST_USER_ID)
        user_2 = DbUser(id=self.TEST_USER_ID_2)

        wallet._set_balance(user_1, self._connection.session, 5)
        wallet._set_balance(user_2, self._connection.session, 5)

        wallet.send_credits(user_1, user_2, 2)
        self.assertEqual(wallet.get_balance(user_1, self._connection.session), 3)
        self.assertEqual(wallet.get_balance(user_2, self._connection.session), 7)
