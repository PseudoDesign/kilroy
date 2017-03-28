from test_connections import TestConnection
from kilroy.connections import DiscordConnection, DiscordMessage, DiscordChannel
from kilroy.user import DiscordUser
from test_user import TestUser
import unittest


class DiscordTestInfo:
    CONNECTION_CLASS = DiscordConnection
    TEST_CHANNEL_INFO = {
        "server_id":288110719428460555,
        "channel_id":288123942722600960,
    }


class TestDiscordConnection(DiscordTestInfo, TestConnection, unittest.TestCase):
    MESSAGE_CLASS = DiscordMessage
    CHANNEL_CLASS = DiscordChannel

    def _test_send_and_receive_private_message(self):
        pass


class TestDiscordUser(DiscordTestInfo, TestUser, unittest.TestCase):
    CONNECTION_CLASS = DiscordConnection
    TEST_USER_NAME = "tense-bot"
    TEST_MENTION_TEXT = "<@293209058679193601>"
