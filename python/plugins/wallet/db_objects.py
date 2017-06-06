from kilroy.db import SqlBase
from kilroy.db.object import SqlObjectInterface
from kilroy.db.db_user import DbUser


class Balance(SqlBase, SqlObjectInterface):
    __tablename__ = "wallet_balance"

    
