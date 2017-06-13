from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime
from sqlalchemy.dialects import sqlite
from datetime import datetime


# sqlite doesn't support BigInteger auto-increment primary keys.  Map it to Integer, just for testing
BigInt = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class UserBalance(SqlBase, SqlObjectInterface):
    __tablename__ = "wallet_balance"

    user_id = Column(BigInt, ForeignKey('user.id'), primary_key=True)
    balance = Column(BigInt, default=0, nullable=False)


class Transaction(SqlBase, SqlObjectInterface):
    __tablename__ = "wallet_transaction"

    id = Column(BigInt, primary_key=True, autoincrement=True)
    source_user = Column(BigInt, ForeignKey('user.id'), nullable=False)
    destination_user = Column(BigInt, ForeignKey('user.id'), nullable=False)
    amount = Column(BigInt, nullable=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
