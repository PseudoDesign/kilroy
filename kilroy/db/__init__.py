from sqlalchemy.ext.declarative import declarative_base
SqlBase = declarative_base()

from .user import User
from .connection import SqlConnection