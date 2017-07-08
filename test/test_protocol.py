"""
Tests for interaction with db for slogans
"""
from socket import socketpair

import asynctest

from server.protocol import SloganProtocol
from server.util import random_string


class ProtocolTest(asynctest.TestCase):

    def setUp(self):
        self.rsock, self.wsock = socketpair()
        self.coro = self.loop.create_connection(SloganProtocol, sock=self.rsock)
        _, self.protocol = self.loop.run_until_complete(self.coro)

    def tearDown(self):
        self.rsock.close()
        self.wsock.close()
        self.coro.close()

    def test_status(self):
        num_slogans, num_rents = self.loop.run_until_complete(self.protocol.status())
        assert isinstance(num_rents, int)
        assert isinstance(num_slogans, int)

    def test_add(self):
        slogan = random_string()
        res = self.loop.run_until_complete(self.protocol.add(slogan))
        assert res == slogan
        res = self.loop.run_until_complete(self.protocol.add(slogan))
        assert res == 'error: slogan already exists'

    def test_rent(self):
        slogan = random_string()
        self.loop.run_until_complete(self.protocol.add(slogan))
        status = self.loop.run_until_complete(self.protocol.rent())
        assert status is True
