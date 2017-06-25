import asyncio
import os

from server.slogan_manager import SloganManager
from server.client_manager import ClientManager


def pytest_configure():
    os.environ['PG_DATABASE'] = os.environ.get('PG_DATABASE', 'slogan_test')
    os.environ['PG_PASSWORD'] = os.environ.get('PG_PASSWORD', '')

    async def init_db():
        await SloganManager().init()
        await ClientManager().init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
