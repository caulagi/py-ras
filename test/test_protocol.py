"""
Tests for interaction with db for slogans
"""
import asynctest

from socket import socketpair

from server.protocol import SloganProtocol


class ProtocolTest(asynctest.TestCase):

    def test_protocol(self):
        rsock, wsock = socketpair()
        coro = self.loop.create_connection(SloganProtocol, sock=rsock)
        transport, protocol = self.loop.run_until_complete(coro)
        num_slogans, num_rents = self.loop.run_until_complete(protocol.status())
        assert isinstance(num_rents, int)
        assert isinstance(num_slogans, int)
        rsock.close()
        wsock.close()
        coro.close()
