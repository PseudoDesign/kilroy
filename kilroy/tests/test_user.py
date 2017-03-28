from kilroy.user import User


class TestUser:

    CONNECTION_CLASS = None
    TEST_USER_NAME = None

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.connection = self.CONNECTION_CLASS()
        self.tasks = []

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

    def test_get_self_user_info(self):
        await def go():
            user_info = connection.get_user_info()
            self.assertEqual(user_info.get_name(), self.TEST_USER_NAME)

            await connection.end_connection()

        connection = self.CONNECTION_CLASS()
        self.tasks += [
            self.loop.create_task(connection.start_connection()),
            self.loop.create_task(go()),
        ]
        self.loop.run_until_complete(asyncio.wait(tasks))
