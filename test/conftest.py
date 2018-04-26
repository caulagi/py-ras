import asyncio
import os

import asyncpg


def pytest_configure():
    # environment should be set before importing
    from server.const import PG_DATABASE, PG_PASSWORD, connection_url
    os.environ['PG_DATABASE'] = PG_DATABASE
    os.environ['PG_PASSWORD'] = PG_PASSWORD

    from server.client_manager import ClientManager
    from server.slogan_manager import SloganManager

    async def init_db():
        await SloganManager().init()
        await ClientManager().init()
        conn = await asyncpg.connect(connection_url())
        await conn.execute('DROP DATABASE IF EXISTS slogan_test')
        await conn.execute('CREATE DATABASE slogan_test')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
