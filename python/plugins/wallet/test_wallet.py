import unittest
from plugins import wallet
from kilroy.db.db_user import DbUser
from tests.test_db import TestDbConnection


class TestWallet(unittest.TestCase, TestDbConnection):
    TEST_USER_ID = 2
    TEST_USER_ID_2 = 5

    def test_get_balance(self):
        # Should be 0 since the user didn't exist before now
        user = DbUser(id=self.TEST_USER_ID)
        balance = wallet.get_balance(user, self._connection)
        self.assertEqual(0, balance)
