import unittest
from kilroy.db.user import DbUser
from tests.test_db import TestDbConnection
from plugins import wallet
from plugins.wallet.db_objects import Transaction


class TestWallet(TestDbConnection, unittest.TestCase):
    TEST_USER_ID = 2
    TEST_USER_ID_2 = 5

    def test_get_and_set_balance(self):
        # Should be 0 by default since the user didn't exist before now
        user = DbUser(id=self.TEST_USER_ID)
        balance = wallet.ops.get_balance(self._connection.session, user)
        self.assertEqual(0, balance)
        user = DbUser(id=self.TEST_USER_ID_2)
        wallet.ops.set_balance(self._connection.session, user, 5)
        balance = wallet.ops.get_balance(self._connection.session, user)
        self.assertEqual(5, balance)

    def test_transactions(self):
        user_1 = DbUser(id=self.TEST_USER_ID)
        user_2 = DbUser(id=self.TEST_USER_ID_2)

        wallet.ops.set_balance(self._connection.session, user_1, 5)
        wallet.ops.set_balance(self._connection.session, user_2, 5)

        wallet.ops.send_credits(self._connection.session, user_1, user_2, 2)
        self.assertEqual(wallet.ops.get_balance(self._connection.session, user_1), 3)
        self.assertEqual(wallet.ops.get_balance(self._connection.session, user_2), 7)
        t = Transaction.get_from_db_by_id(self._connection.session, 1)
        self.assertEqual(t.source_user, self.TEST_USER_ID)
        self.assertEqual(t.destination_user, self.TEST_USER_ID_2)
        self.assertEqual(t.amount, 2)

        wallet.ops.set_balance(self._connection.session, user_1, 5)
        wallet.ops.set_balance(self._connection.session, user_2, 5)
        with self.assertRaises(ValueError):
            wallet.ops.send_credits(self._connection.session, user_1, user_2, 6)
