import aiohttp
import pytest_asyncio

from redis.asyncio import Redis

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from settings import test_settings


@pytest_asyncio.fixture(name='session_client', scope='session')
async def session_client():
    '''
    Для запросов во внешние системы будет использоваться библиотека aiohttp.
    Фикстура предназначена для создания и управления асинхронной HTTP-сессией,
    которая будет использоваться для выполнения HTTP-запросов во внешних системах.
    '''
    session_client = aiohttp.ClientSession()
    yield session_client
    await session_client.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    '''
    Фикстура для установки соединения с ES.
    '''
    client = AsyncElasticsearch(
        hosts=test_settings.elastic_host,
        verify_certs=False
    )
    yield client
    await client.close()


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


@pytest_asyncio.fixture
def make_get_request(session_client):
    '''
    Фикстура выполнения GET-запросов
    '''
    async def inner(endpoint: str, params: dict = None) -> dict:
        url = test_settings.service_url + endpoint
        params = params or {}
        async with session_client.get(url, params=params) as response:
            return {
                'body': await response.json(),
                'headers': dict(response.headers),
                'status': response.status,
            }
    return inner


@pytest_asyncio.fixture(name='es_data')
def es_data():
    def inner(es_row_data):
        bulk_query: list[dict] = []
        for row in es_row_data:
            data = {'_index': 'index', '_id': row['uuid']}
            data.update({'_source': row})
            bulk_query.append(data)
        return bulk_query
    return inner
