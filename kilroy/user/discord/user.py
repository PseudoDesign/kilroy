from .. import User


class DiscordUser(User):
    def __init__(self, discord_user):
        self.__user = discord_user

    def get_name(self):
        return self.__user.name
