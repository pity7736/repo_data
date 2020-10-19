import asyncio
import os
from unittest.mock import AsyncMock, patch

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from asyncpg.transaction import Transaction
from pytest import fixture
from tortoise import Tortoise

from repo_data import init_db
from tests.factories import UserFactory, RepositoryFactory


@fixture(scope='session')
def event_loop():
    return asyncio.get_event_loop()


@fixture(scope='session')
async def db_pool(session_mocker):
    pool: Pool = await asyncpg.create_pool(
        host=os.environ['REPO_DATA_HOST'],
        user=os.environ['REPO_DATA_USER'],
        database=os.environ['REPO_DATA_DATABASE'],
        password=os.environ['REPO_DATA_PASSWORD'],
        port=int(os.environ['REPO_DATA_PORT']),
        min_size=2
    )
    print('pool created')
    pool_mock = session_mocker.patch.object(
        asyncpg,
        'create_pool',
        new_callable=AsyncMock
    )
    pool_mock.return_value = pool
    await init_db()
    yield pool
    print('closing pool')
    await pool.close()
    print('pool closed')


@fixture
async def db_connection(db_pool, mocker):
    connection: Connection = await db_pool.acquire()
    transaction: Transaction = connection.transaction()
    connect_mock = mocker.patch.object(Pool, 'acquire', new_callable=AsyncMock)
    release_mock = patch.object(Pool, 'release', new_callable=AsyncMock)
    connect_mock.return_value = connection
    release_mock.start()
    await transaction.start()
    await Tortoise.generate_schemas()
    yield connection
    print('doing rollback')
    await transaction.rollback()
    print('rollback done!')
    release_mock.stop()
    print('releasing connection')
    await db_pool.release(connection)


@fixture
async def user_fixture(db_connection):
    return await UserFactory.create()


@fixture
async def repo_fixture(user_fixture):
    return await RepositoryFactory.create(owner=user_fixture)
