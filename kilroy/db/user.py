from . import SqlBase
from sqlalchemy import Column, Integer, String
from .object import SqlObjectInterface


class User(SqlBase, SqlObjectInterface):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    client = Column(String(128), nullable=False)
    unique_id = Column(String(128), nullable=False)
