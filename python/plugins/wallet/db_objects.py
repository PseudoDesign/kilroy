from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from sqlalchemy import Column, Integer, ForeignKey


class UserBalance(SqlBase, SqlObjectInterface):
    __tablename__ = "wallet_balance"

    user = Column(Integer, ForeignKey('user.id'), primary_key=True)
