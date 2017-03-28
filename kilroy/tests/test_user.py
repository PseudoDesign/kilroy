from kilroy.user import User
import asyncio
from time import sleep
from test_connections import ConnectionTestHandler


class TestUser(ConnectionTestHandler):

    CONNECTION_CLASS = None
    TEST_USER_NAME = None
    TEST_MENTION_TEXT = None

    def test_get_self_user_info(self):
        async def go():
            await connection.await_until_connected()
            user_info = connection.get_user_info()
            self.assertIsNotNone(user_info)
            self.assertEqual(user_info.get_name(), self.TEST_USER_NAME)
            self.assertEqual(
                user_info.get_mention_text(),
                self.TEST_MENTION_TEXT
            )
            await connection.end_connection()

        connection = self.CONNECTION_CLASS()
        self.tasks += [
            self.loop.create_task(go())
        ]
        self.run_test(connection)

    def test_get_channel_user_info(self):
        async def go():
            await connection.await_until_connected()


            await connection.end_connection()
