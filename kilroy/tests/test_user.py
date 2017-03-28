from kilroy.user import User
import asyncio
from time import sleep


class ConnectionTestHandler:
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tasks = []

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def run_test(self, connection):
        self.tasks += [self.loop.create_task(connection.start_connection())]
        self.loop.run_until_complete(asyncio.wait(self.tasks))


class TestUser(ConnectionTestHandler):

    CONNECTION_CLASS = None
    TEST_USER_NAME = None

    def test_get_self_user_info(self):
        async def go():
            await connection.await_until_connected()
            user_info = connection.get_user_info()
            self.assertIsNotNone(user_info)
            self.assertEqual(user_info.get_name(), self.TEST_USER_NAME)
            await connection.end_connection()

        connection = self.CONNECTION_CLASS()
        self.tasks += [
            self.loop.create_task(go())
        ]
        self.run_test(connection)
