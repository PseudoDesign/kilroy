from . import SqlBase
from sqlalchemy import Column, Integer, String, BigInteger
from .object import SqlObjectInterface
from sqlalchemy.dialects import sqlite


# sqlite doesn't support BigInteger auto-increment primary keys.  Map it to Integer, just for testing
BigInt = BigInteger().with_variant(sqlite.INTEGER(), 'sqlite')


class DbUser(SqlBase, SqlObjectInterface):
    __tablename__ = "user"

    id = Column(BigInt, primary_key=True)
    client_name = Column(String(128), nullable=False)
    client_id = Column(String(128), nullable=False)
