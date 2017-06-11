from ..db.user import DbUser


class User:

    CLIENT_NAME = None

    def __init__(self, client_user):
        raise NotImplementedError()

    def get_name(self):
        raise NotImplementedError()

    def get_mention_text(self):
        raise NotImplementedError()

    def get_id(self):
        """
        Return the client-unique ID for this user
        :return: str
        """
        raise NotImplementedError()

    def get_db_obj(self, db_session):
        """
        Returns the db object for this user
        :return: kilroy.db.user.User
        """
        ret = DbUser.get_from_db_by_kwargs(db_session, client_name=self.CLIENT_NAME, client_id=self.get_id())
        if ret is not None:
            return ret
        ret = DbUser(client_name=self.CLIENT_NAME, client_id=self.get_id())
        ret.write_to_db(db_session)
        return ret

