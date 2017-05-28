class User:
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

    def get_db_obj(self):
        """
        Returns the db object for this user
        :return: kilroy.db.user.User
        """
        raise NotImplementedError()
