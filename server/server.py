'''
rent-a-slogan socket server

    * listens on port 25001 and opens a socket for each new client
    * allows clients to add slogan
    * allows clients to ask for status
    * allows clients to rent one slogan for 15 seconds
'''
import argparse
import asyncio
import gc

import uvloop

from .client_manager import ClientManager
from .protocol import SloganProtocol
from .slogan_manager import SloganManager


async def initialize_tables():
    sm = SloganManager()
    await sm.init()
    await sm.expire_slogans()
    cm = ClientManager()
    await cm.init()
    await cm.deactivate_all()


async def print_debug(loop):
    while True:
        loop.print_debug_info()
        await asyncio.sleep(2, loop=loop)


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=25001, type=int)
    parser.add_argument('--debug', default=False, action='store_true')
    args = parser.parse_args()

    loop = uvloop.new_event_loop()
    print('using UVLoop')
    asyncio.set_event_loop(loop)

    loop.set_debug(args.debug)
    # if hasattr(loop, 'print_debug_info'):
    #     loop.create_task(print_debug(loop))

    coro = loop.create_server(SloganProtocol, *('127.0.0.1', args.port))
    loop.run_until_complete(coro)
    loop.run_until_complete(initialize_tables())
    print('serving on: 127.0.0.1:{}'.format(args.port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        if hasattr(loop, 'print_debug_info'):
            gc.collect()
            if args.debug:
                loop.print_debug_info()
        loop.close()
