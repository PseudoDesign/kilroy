from .. import User
from db.user import User as DbUser


class DiscordUser(User):
    def __init__(self, discord_user):
        self.__user = discord_user

    def get_name(self):
        return self.__user.name

    def get_mention_text(self):
        return self.__user.mention

    def get_id(self):
        return self.__user.id

    def get_db_obj(self):
        return DbUser(client_name='discord', client_id=self.get_id())
