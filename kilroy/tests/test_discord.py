from test_connections import TestConnection
from kilroy.connections import DiscordConnection, DiscordMessage, DiscordChannel
from kilroy.user import DiscordUser
from test_user import TestUser
import unittest

class TestDiscordConnection(TestConnection, unittest.TestCase):
    CONNECTION_CLASS = DiscordConnection
    MESSAGE_CLASS = DiscordMessage
    CHANNEL_CLASS = DiscordChannel
    TEST_CHANNEL_INFO = {
        "server_id":288110719428460555,
        "channel_id":288123942722600960,
    }

    def _test_send_and_receive_private_message(self):
        pass

class TestDiscordUser(TestUser, unittest.TestCase):
    CONNECTION_CLASS = DiscordConnection
    TEST_USER_NAME = "tense-bot"
