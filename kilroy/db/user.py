from . import SqlBase
from sqlalchemy import Column, Integer
from .object import SqlObjectInterface


class User(SqlBase, SqlObjectInterface):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)