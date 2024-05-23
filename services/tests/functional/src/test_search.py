import pytest
import json


@pytest.mark.asyncio(scope='session')
async def test_film_search(make_get_request):
    query_data = {"query": "Wars"}
    response = await make_get_request(f'films/search/', query_data)
    assert response['status'] == 200
    assert len(response['body']) == 10


@pytest.mark.asyncio(scope='session')
async def test_film_search_n_size(make_get_request, redis_client):
    cache_key = 'film:query:star'
    await redis_client.delete(cache_key)

    query_data = {"query": "Star", "page": 1, "size": 5}
    response = await make_get_request(f'films/search/', query_data)

    assert response['status'] == 200
    assert len(response['body']) == 5


@pytest.mark.asyncio(scope='session')
async def test_film_search_n_size_cache(make_get_request, redis_client):
    cache_key = 'film:query:star'
    await redis_client.delete(cache_key)

    query_data = {"query": "Star", "page": 1, "size": 2}
    response = await make_get_request(f'films/search/', query_data)

    cache = await redis_client.get(cache_key)
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache
