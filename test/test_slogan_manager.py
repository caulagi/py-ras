"""
Tests for interaction with db for slogans
"""
import asyncio
import random
import string
from unittest import TestCase

import asyncpg

from server.const import connection_url
from server.slogan_manager import SloganManager


class SloganManagerTest(TestCase):

    @staticmethod
    def random_title():
        return ''.join(random.choice(string.ascii_lowercase) for i in range(20))

    @classmethod
    def setUpClass(cls):
        cls.sm = SloganManager()
        cls.loop = asyncio.get_event_loop()

    def test_debug(self):
        assert connection_url() == ''

    async def _test_init(self):
        await self.sm.init()
        conn = await asyncpg.connect(connection_url())
        row = await conn.fetchrow(
            'select table_name from information_schema.tables where table_name = \'slogan\''
        )
        assert row['table_name'] == 'slogan'

    def test_init(self):
        self.loop.run_until_complete(self._test_init())

    def test_md5(self):
        assert SloganManager.get_md5('test') == '098f6bcd4621d373cade4e832627b4f6'

    async def _test_create(self):
        title = self.random_title()
        ok, res = await self.sm.create(title)
        assert ok is True
        assert res == title

    def test_create(self):
        self.loop.run_until_complete(self._test_create())

    async def _test_create_unique_constraint(self):
        title = self.random_title()
        await self.sm.create(title)
        ok, _ = await self.sm.create(title)
        assert ok is False

    def test_create_unique_constraint(self):
        self.loop.run_until_complete(self._test_create_unique_constraint())

    async def _test_rent_when_available(self):
        title = self.random_title()
        await self.sm.create(title)
        status, _ = await self.sm.rent(rented_by=title)
        assert status is True

    def test_rent_when_available(self):
        self.loop.run_until_complete(self._test_rent_when_available())

    # def test_rent_none_available(self):
    #     with NamedTemporaryFile() as test_db:
    #         slogan_manager = SloganManager(test_db.name)
    #         slogan_manager.create('test')
    #         slogan_manager.rent()
    #         status, _ = slogan_manager.rent()
    #         assert status is False

    # def test_list(self):
    #     with NamedTemporaryFile() as test_db:
    #         slogan_manager = SloganManager(test_db.name)
    #         slogan_manager.create('test 1')
    #         slogan_manager.create('test 2')
    #         assert len(slogan_manager.list()) == 2
