from . import SqlBase
from sqlalchemy import Column, Integer, String
from .object import SqlObjectInterface


class DbUser(SqlBase, SqlObjectInterface):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    client_name = Column(String(128), nullable=False)
    client_id = Column(String(128), nullable=False)
