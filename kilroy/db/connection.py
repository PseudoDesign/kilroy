from threading import Lock
from . import SqlBase
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class SqlConnection:

    SqlSession = sessionmaker()

    def __init__(self, db='sqlite:///:memory:', echo=False):
        self.__db = db
        self.__echo = echo
        self.__engine = None
        self.__engine_lock = Lock()
        self.session = None
        self.reset_engine()

    def __del__(self):
        self.close_connection()

    def reset_engine(self):
        # Can be used to reset an sqlite database in memory.  Useful for testing
        with self.__engine_lock:
            self.__engine = create_engine(self.__db, echo=self.__echo)
            SqlBase.metadata.bind = self.__engine
            self.SqlSession.configure(bind=self.__engine)

    def start_connection(self):
        with self.__engine_lock:
            if self.session is None:
                self.session = self.SqlSession()
            else:
                raise ValueError("Connection is already open")

    def close_connection(self):
        with self.__engine_lock:
            if self.session is not None:
                self.session.close()
                self.session = None

    def create_tables(self):
        with self.__engine_lock:
            SqlBase.metadata.create_all(self.__engine)

    def get_tables_in_db(self):
        with self.__engine_lock:
            return self.__engine.table_names()
