from sqlalchemy.ext.declarative import declarative_base
SqlBase = declarative_base()

from .db_user import DbUser
from .connection import SqlConnection