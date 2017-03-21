import asyncio


class Connection:
    def __init__(self, **kwargs):
        pass

    async def await_until_connected(self):
        await asyncio.sleep(.2)
        return True
