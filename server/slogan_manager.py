'''
The slogan manager is the interface between python
and sqlite for the slogan table
'''
import hashlib
from datetime import datetime, timedelta

import asyncpg
import pytz

from .const import connection_url


class SloganManager(object):
    '''
    The slogan table has -
        title (text) - the actual slogan
        md5 (text) - used to ensure uniqueness
        rented_on (datetime) - if the slogan is rented, the datetime field
        rented_by (text) - socket identifier
    '''

    EXPIRE_AFTER_SECONDS = 15

    async def init(self):
        conn = await asyncpg.connect(connection_url())
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS slogan (
                id           SERIAL PRIMARY KEY,
                title        TEXT,
                md5          TEXT UNIQUE,
                rented_on    TIMESTAMPTZ NULL,
                rented_by    TEXT UNIQUE NULL
            );
        ''')
        self._initialized = True

    @staticmethod
    def get_md5(title):
        h = hashlib.md5()  # nosec
        h.update(title.encode('utf-8'))
        return h.hexdigest()

    async def create(self, title):
        'Store the slogan identified by the title to database.  Return a tuple of (status, title)'
        conn = await asyncpg.connect(connection_url())
        try:
            await conn.execute(
                'INSERT INTO slogan (title, md5, rented_by, rented_on) VALUES ($1, $2, $3, $4)',
                title, self.get_md5(title), None, None)
        except asyncpg.PostgresError as e:
            print(e)
            return (False, 'error: slogan already exists')
        finally:
            await conn.close()
        return (True, title)

    async def expire(self, slogan_id):
        conn = await asyncpg.connect(connection_url())
        await conn.execute(
            'UPDATE slogan SET rented_on = NULL, rented_by = NULL WHERE id = $1',
            slogan_id)

    async def expire_slogans(self, conn=None):
        if not conn:
            conn = await asyncpg.connect(connection_url())
        async with conn.transaction():
            await conn.execute(
                'UPDATE slogan SET rented_on = NULL, rented_by = NULL WHERE rented_on < $1',
                datetime.utcnow().replace(tzinfo=pytz.utc) - timedelta(seconds=self.EXPIRE_AFTER_SECONDS))

    async def _find_rent(self, conn, rented_by):
        async with conn.transaction():
            await conn.execute(
                'UPDATE slogan SET rented_on = $1, rented_by = $2 WHERE id = (SELECT id FROM slogan WHERE rented_on IS NULL LIMIT 1)',
                datetime.utcnow().replace(tzinfo=pytz.utc), rented_by)
            return await conn.fetchrow('SELECT id, title FROM slogan WHERE rented_by = $1', rented_by)

    async def _allow_renting(self, conn, rented_by):
        has_rented = await conn.fetchrow('SELECT 1 FROM slogan WHERE rented_by = $1', rented_by)
        if has_rented:
            return False
        rent_available = await conn.fetchrow('SELECT 1 FROM slogan WHERE rented_on IS NULL')
        if rent_available:
            return True
        return False

    async def rent(self, rented_by):
        'Find any available slogan to rent. Return a tuple of (status, title)'
        conn = await asyncpg.connect(connection_url())
        await self.expire_slogans(conn)
        status = await self._allow_renting(conn, rented_by)
        if not status:
            return (False, 'error: Can\'t rent at this time')
        row = await self._find_rent(conn, rented_by)
        await conn.close()
        return (True, row)

    async def list(self):
        conn = await asyncpg.connect(connection_url())
        num_slogans = await conn.fetchval('select count(*) from slogan')
        num_rents = await conn.fetchval('select count(*) from slogan where rented_on is not null')
        return (True, (num_slogans, num_rents))
