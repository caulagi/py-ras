import asyncio
import os


def pytest_configure():
    # environment should be set before importing
    os.environ['PG_DATABASE'] = os.environ.get('PG_DATABASE', 'slogan_test')
    os.environ['PG_PASSWORD'] = os.environ.get('PG_PASSWORD', '')

    from server.client_manager import ClientManager
    from server.slogan_manager import SloganManager

    async def init_db():
        await SloganManager().init()
        await ClientManager().init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
