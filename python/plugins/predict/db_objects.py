from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, String
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