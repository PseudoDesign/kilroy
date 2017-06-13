from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from sqlalchemy import Column, Integer, ForeignKey, BigInteger
from sqlalchemy.dialects import sqlite


# sqlite doesn't support BigInteger auto-increment primary keys.  Map it to Integer, just for testing
BigInt = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class UserBalance(SqlBase, SqlObjectInterface):
    __tablename__ = "wallet_balance"

    user_id = Column(BigInt, ForeignKey('user.id'), primary_key=True)
    balance = Column(BigInt, default=0)
