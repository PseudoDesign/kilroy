import unittest

from test_connections import TestConnection
from test_user import TestUser

from kilroy.connections import DiscordConnection, DiscordMessage, DiscordChannel


class DiscordTestInfo:
    CONNECTION_CLASS = DiscordConnection
    TEST_CHANNEL_INFO = {
        "server_id": 410949404590080000,
        "channel_id": 410949404590080002,
    }


class TestDiscordConnection(DiscordTestInfo, TestConnection, unittest.TestCase):
    MESSAGE_CLASS = DiscordMessage
    CHANNEL_CLASS = DiscordChannel

    def _test_send_and_receive_private_message(self):
        pass


class TestDiscordUser(DiscordTestInfo, TestUser, unittest.TestCase):
    TEST_USER_NAME = "tense-bot"
    TEST_MENTION_TEXT = "<@293209058679193601>"
    TEST_USER_ID = "293209058679193601"
    TEST_CLIENT_NAME = "discord"
