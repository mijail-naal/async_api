import pytest_asyncio

from elasticsearch import AsyncElasticsearch

from settings import test_settings


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
