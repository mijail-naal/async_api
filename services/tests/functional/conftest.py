import aiohttp
import pytest_asyncio

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from redis.asyncio import Redis

from tests.functional.settings import test_settings


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=test_settings.es_host, verify_certs=False)
    yield client
    await client.close()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict]):
        if await es_client.indices.exists(index=test_settings.es_index):
            await es_client.indices.delete(index=test_settings.es_index)
        await es_client.indices.create(index=test_settings.es_index, **test_settings.es_index_mapping)
        updated, errors = await async_bulk(client=es_client, actions=data)
        if errors:
            raise Exception('Ошибка записи данных в Elasticsearch')
    return inner


@pytest_asyncio.fixture(name='session_client', scope='session')
async def session_client():
    session_client = aiohttp.ClientSession()
    yield session_client
    await session_client.close()


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(session_client):
    async def inner(endpoint: str, query_data: dict = None):
        url = test_settings.service_url + endpoint
        query_data = query_data
        async with session_client.get(url, params=query_data) as response:
            return dict(
                body = await response.json(),
                headers = response.headers,
                status = response.status
            )
    return inner


@pytest_asyncio.fixture(name='redis_client', scope='session')
async def redis_client():
    client = Redis(
        host=test_settings.redis_host, 
        port=test_settings.redis_port, 
        decode_responses=True)
    yield client
    await client.aclose()


@pytest_asyncio.fixture(name='es_data')
def es_data():
    def inner(es_row_data):
        bulk_query: list[dict] = []
        for row in es_row_data:
            data = {'_index': 'test_movies', '_id': row['uuid']}
            data.update({'_source': row})
            bulk_query.append(data)
        return bulk_query
    return inner