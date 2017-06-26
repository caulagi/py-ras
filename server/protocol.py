'''
rent-a-slogan socket server

    * listens on port 25001 and opens a socket for each new client
    * allows clients to add slogan
    * allows clients to ask for status
    * allows clients to rent one slogan for 15 seconds
'''
import asyncio
from functools import partial

from .client_manager import ClientManager
from .slogan_manager import SloganManager
from .util import random_string

CLRF = '\r\n'


class SloganProtocol(asyncio.Protocol):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.identifier = random_string()
        self.slogan_manager = SloganManager()
        self.client_manager = ClientManager()

    def connection_made(self, transport):
        print('new connection: {}'.format(transport.get_extra_info('socket')))
        self.transport = transport
        asyncio.ensure_future(self.add_client())

    def connection_lost(self, exc):
        print('closed connection: {}'.format(self.transport.get_extra_info('socket')))
        self.transport = None
        self.slogan_manager = None
        self.client_manager = None
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
        status, res = await self.slogan_manager.list()
        if not status:
            self.transport.write('error getting details {}'.format(CLRF).encode())
            return
        num_slogans, num_rents = res
        self.transport.write('Number of slogans: {}{}'.format(num_slogans, CLRF).encode())
        self.transport.write('Number of rents: {}{}'.format(num_rents, CLRF).encode())
        await self.status_clients()
        return (num_slogans, num_rents)

    async def status_clients(self):
        status, num_clients = await self.client_manager.count()
        if not status:
            self.transport.write('error getting client details {}'.format(CLRF).encode())
            return
        self.transport.write('Number of clients: {}{}'.format(num_clients, CLRF).encode())

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
