import aiohttp
import pytest_asyncio

from settings import test_settings


@pytest_asyncio.fixture(name='session_client', scope='session')
async def session_client():
    '''The aiohttp library will be used for requests to external systems.

    The fixture is designed to create and manage an asynchronous HTTP session 
    that will be used to execute HTTP requests in external systems.
    '''
    session_client = aiohttp.ClientSession()
    yield session_client
    await session_client.close()


@pytest_asyncio.fixture
def make_get_request(session_client):
    '''Fixture for executing GET requests.'''
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
