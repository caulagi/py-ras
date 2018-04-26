import asyncio
import os

import asyncpg


def pytest_configure():
    # environment should be set before importing
    os.environ['PG_DATABASE'] = 'slogan_test'

    from server.client_manager import ClientManager
    from server.const import connection_url
    from server.slogan_manager import SloganManager

    async def init_db():
        await SloganManager().init()
        await ClientManager().init()
        conn = await asyncpg.connect(connection_url())
        await conn.execute('DROP DATABASE IF EXISTS %s' % os.environ['PG_DATABASE'])
        await conn.execute('CREATE DATABASE slogan_test')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
