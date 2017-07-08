"""
Tests for interaction with db for slogans
"""
import asyncio

from asynctest import TestCase

from server.client_manager import ClientManager
from server.util import random_string


class ClientManagerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cm = ClientManager()
        cls.loop = asyncio.get_event_loop()

    def test_count(self):
        async def _test_count(self):
            await self.cm.create(1, random_string())
            return await self.cm.count()
        status, num_clients = self.loop.run_until_complete(_test_count(self))
        assert status is True
        assert num_clients > 0
