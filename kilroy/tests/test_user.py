from kilroy.user import User
import asyncio
from time import sleep
from test_connections import ConnectionTestHandler


class TestUser(ConnectionTestHandler):

    CONNECTION_CLASS = None
    TEST_USER_NAME = None
    TEST_MENTION_TEXT = None
    TEST_CHANNEL_INFO = None
    TEST_USER_ID = None

    def test_get_self_user_info(self):
        async def go():
            await connection.await_until_connected()
            self.user_info = connection.get_user_info()
            self.mention_text = self.user_info.get_mention_text()
            self.name = self.user_info.get_name()
            self.user_id = self.user_info.get_id()

            await connection.end_connection()

        connection = self.CONNECTION_CLASS(**self.connection_config_data)
        self.tasks += [
            self.loop.create_task(go())
        ]
        self.run_test(connection)
        self.assertIsNotNone(self.user_info)
        self.assertEqual(self.name, self.TEST_USER_NAME)
        self.assertEqual(self.user_id, self.TEST_USER_ID)
        self.assertEqual(
            self.mention_text,
            self.TEST_MENTION_TEXT
        )

    def test_get_channel_user_info(self):
        async def go():
            await connection.await_until_connected()
            channel = connection.get_channel_from_kwargs(**self.TEST_CHANNEL_INFO)
            users = channel.get_users()
            self.found_self = False
            for user in users:
                if user.get_mention_text() == self.TEST_MENTION_TEXT:
                    self.found_self = True
                    break
            await connection.end_connection()

        connection = self.CONNECTION_CLASS(**self.connection_config_data)
        self.tasks += [
            self.loop.create_task(go())
        ]
        self.run_test(connection)
        self.assertTrue(self.found_self)

    def test_create_db_user_object(self):
        async def go():
            await connection.await_until_connected()
            self.user_info = connection.get_user_info()
            self.db_obj = self.user_info.get_db_obj()

            await connection.end_connection()

        connection = self.CONNECTION_CLASS(**self.connection_config_data)
        self.tasks += [
            self.loop.create_task(go())
        ]
        self.run_test(connection)
        self.assertEqual(self.db_obj.client_id, self.TEST_USER_ID)
        self.assertEqual(self.db_obj.client_name, self.TEST_CLIENT_NAME)

