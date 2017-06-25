'''
rent-a-slogan socket server

    * listens on port 25001 and opens a socket for each new client
    * allows clients to add slogan
    * allows clients to ask for status
    * allows clients to rent one slogan for 15 seconds
'''
import asyncio
import random
import string
from functools import partial

from .client_manager import ClientManager
from .slogan_manager import SloganManager

CLRF = '\r\n'


class SloganProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.identifier = ''.join(random.choice(string.ascii_lowercase) for i in range(8))  # nosec

    def connection_made(self, transport):
        print('new connection: {}'.format(transport.get_extra_info('socket')))
        self.transport = transport
        self.slogan_manager = SloganManager()
        self.client_manager = ClientManager()
        asyncio.ensure_future(self.add_client())

    def connection_lost(self, exc):
        print('closed connection: {}'.format(self.transport.get_extra_info('socket')))
        self.transport = None
        self.slogan_manager = None
        asyncio.ensure_future(self.deactivate_client())

    def data_received(self, data):
        data = data.decode()
        try:
            cmd, rest = data.split('::')
        except ValueError:
            cmd, rest = (data, '')
        cmd, rest = cmd.strip(), rest.strip()
        self.run_cmd(cmd, rest)

    async def add_client(self):
        sock = self.transport.get_extra_info('socket')
        await self.client_manager.create(sock.fileno(), self.identifier)

    async def deactivate_client(self):
        await self.client_manager.deactivate(self.identifier)

    async def status(self):
        res = await self.slogan_manager.list()
        self.transport.write('Slogans: {}'.format(CLRF).encode())
        self.transport.write(CLRF.join(res).encode())
        self.transport.write(CLRF.encode())
        asyncio.ensure_future(self.status_clients())

    async def status_clients(self):
        res = await self.client_manager.list()
        self.transport.write('Clients: {}'.format(CLRF).encode())
        self.transport.write(CLRF.join(res).encode())
        self.transport.write(CLRF.encode())

    async def rent(self):
        status, res = await self.slogan_manager.rent(self.identifier)
        if not status:
            self.transport.write('{}{}'.format(res, CLRF).encode())
            return
        self.transport.write('OK: id:{} title:{}'.format(res['id'], res['title']).encode())
        self.transport.write(CLRF.encode())
        self.loop.call_later(self.slogan_manager.EXPIRE_AFTER_SECONDS,
                             partial(self.expire_rent, res['id']))

    def expire_rent(self, slogan_id):
        asyncio.ensure_future(self.expire_rent_async(slogan_id))

    async def expire_rent_async(self, slogan_id):
        await self.slogan_manager.expire(slogan_id)
        self.transport.write('Slogan id {} has expired'.format(slogan_id).encode())
        self.transport.write(CLRF.encode())

    async def add(self, slogan):
        _, res = await self.slogan_manager.create(slogan)
        self.transport.write(res.encode())
        self.transport.write(CLRF.encode())

    def run_cmd(self, cmd, slogan=None):
        cmd = cmd.lower()
        if cmd == 'add':
            asyncio.ensure_future(self.add(slogan))
        elif cmd == 'status':
            asyncio.ensure_future(self.status())
        elif cmd == 'rent':
            asyncio.ensure_future(self.rent())
