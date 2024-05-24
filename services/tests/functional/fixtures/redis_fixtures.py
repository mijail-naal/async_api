import pytest_asyncio

from redis.asyncio import Redis

from settings import test_settings


@pytest_asyncio.fixture(name='redis_client', scope='session')
async def redis_client():
    '''
    Фикстура для установки соединения с Redis.
    При этом каждый раз будет происходить сброс кэша.
    '''
    client = Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        decode_responses=True)
    await client.flushdb(asynchronous=True)
    yield client
    await client.aclose()
