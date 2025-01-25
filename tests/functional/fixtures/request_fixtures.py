import aiohttp
import pytest_asyncio

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
