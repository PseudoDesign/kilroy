from .. import User


class DiscordUser(User):

    CLIENT_NAME = "discord"

    def __init__(self, discord_user):
        self.__user = discord_user

    def get_name(self):
        return self.__user.name

    def get_mention_text(self):
        return self.__user.mention

    def get_id(self):
        return self.__user.id
