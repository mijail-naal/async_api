import json
import pytest


@pytest.mark.asyncio(scope='session')
async def test_genre_details(make_get_request):
    query_data = '3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff'
    response = await make_get_request(f'genres/{query_data}')

    assert response['status'] == 200
    assert len(response['body']) == 2
    assert response['body']['name'] == 'Action'
    assert response['body']['uuid'] == query_data


@pytest.mark.asyncio(scope='session')
async def test_genre_not_found(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-@-¿+-no-exists-id'
    response = await make_get_request(f'genre/{query_data}')

    assert response['status'] == 404
    assert response['body'] == {"detail":"Not Found"}


@pytest.mark.asyncio(scope='session')
async def test_genre_list(make_get_request):
    response = await make_get_request(f'genres')

    assert response['status'] == 200
    assert len(response['body']) == 26


@pytest.mark.asyncio(scope='session')
async def test_genre_cache(make_get_request, redis_client):
    cache_key = 'genre:all'
    await redis_client.delete(cache_key)

    response = await make_get_request(f'genres')

    cache = await redis_client.get(cache_key)
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache

