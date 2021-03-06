from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, String, Boolean, SmallInteger
from sqlalchemy.dialects import sqlite
from datetime import datetime


# sqlite doesn't support BigInteger auto-increment primary keys.  Map it to Integer, just for testing
BigInt = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class Market(SqlBase, SqlObjectInterface):
    __tablename__ = "predict_market"

    id = Column(BigInt, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    yes_option = Column(String(256), nullable=False)
    no_option = Column(String(256), nullable=False)
    expiration = Column(DateTime, nullable=False)
    facilitator_id = Column(BigInt, ForeignKey('user.id'), nullable=False)


class BuyOrder(SqlBase, SqlObjectInterface):
    __tablename__ = "predict_buy_order"

    id = Column(BigInt, primary_key=True, autoincrement=True)
    market_id = Column(BigInt, ForeignKey('predict_market.id'), nullable=False)
    option = Column(Boolean, nullable=False)
    price = Column(SmallInteger, nullable=False)
    expiration = Column(DateTime, nullable=False)
    user_id = Column(BigInt, ForeignKey('user.id'), nullable=False)
    quantity = Column(SmallInteger, nullable=False)
    filled_quantity = Column(SmallInteger, default=0, nullable=False)

    @property
    def remaining_quantity(self):
        return self.quantity - self.filled_quantity


class Transaction(SqlBase, SqlObjectInterface):
    __tablename__ = "predict_transaction"

    id = Column(BigInt, primary_key=True, autoincrement=True)
    yes_holder_id = Column(BigInt, ForeignKey('user.id'), nullable=False)
    no_holder_id = Column(BigInt, ForeignKey('user.id'), nullable=False)
    buy_order_id = Column(BigInt, ForeignKey('predict_buy_order.id'), nullable=False)
    quantity = Column(SmallInteger, nullable=False)
