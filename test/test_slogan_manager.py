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
        return ''.join(random.choice(string.ascii_lowercase) for i in range(20))  # nosec

    @classmethod
    def setUpClass(cls):
        cls.sm = SloganManager()
        cls.loop = asyncio.get_event_loop()

    def test_init(self):
        async def _test_init(self):
            conn = await asyncpg.connect(connection_url())
            row = await conn.fetchrow(
                'select table_name from information_schema.tables where table_name = \'slogan\''
            )
            assert row['table_name'] == 'slogan'
        self.loop.run_until_complete(_test_init(self))

    # pylint: disable=R0201
    def test_md5(self):
        assert SloganManager.get_md5('test') == '098f6bcd4621d373cade4e832627b4f6'

    def test_create(self):
        async def _test_create(self):
            title = self.random_title()
            ok, res = await self.sm.create(title)
            assert ok is True
            assert res == title
        self.loop.run_until_complete(_test_create(self))

    def test_create_unique_constraint(self):
        async def _test_create_unique_constraint(self):
            title = self.random_title()
            await self.sm.create(title)
            ok, _ = await self.sm.create(title)
            assert ok is False
        self.loop.run_until_complete(_test_create_unique_constraint(self))

    def test_rent_when_available(self):
        async def _test_rent_when_available(self):
            title = self.random_title()
            await self.sm.create(title)
            status, _ = await self.sm.rent(rented_by=title)
            assert status is True
        self.loop.run_until_complete(_test_rent_when_available(self))

    # def test_rent_none_available(self):
    #     with NamedTemporaryFile() as test_db:
    #         slogan_manager = SloganManager(test_db.name)
    #         slogan_manager.create('test')
    #         slogan_manager.rent()
    #         status, _ = slogan_manager.rent()
    #         assert status is False

    def test_list(self):
        async def _test_list(self):
            title = self.random_title()
            await self.sm.create(title)
            return await self.sm.list()
        status, res = self.loop.run_until_complete(_test_list(self))
        assert status is True
        assert res[0] > 0
        assert len(res) == 3
