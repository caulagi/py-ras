import asyncio
import os

import asyncpg


def pytest_configure():
    # environment should be set before importing
    os.environ['PG_DATABASE'] = 'slogan_test'

    from server.client_manager import ClientManager
    from server.const import PG_USERNAME, PG_PASSWORD
    from server.slogan_manager import SloganManager

    async def init_db():
        conn = await asyncpg.connect(user=PG_USERNAME, password=PG_PASSWORD)
        await conn.execute('DROP DATABASE IF EXISTS %s' % os.environ['PG_DATABASE'])
        await conn.execute('CREATE DATABASE slogan_test')
        await SloganManager().init()
        await ClientManager().init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
