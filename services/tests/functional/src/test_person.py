import json
import pytest
import http

@pytest.mark.asyncio(scope='session')
async def test_person_details(make_get_request):
    query_data = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'
    response = await make_get_request(f'persons/{query_data}')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 3
    assert response['body']['uuid'] == query_data


@pytest.mark.asyncio(scope='session')
async def test_person_not_found(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-@-¿+-no-exists-id'
    response = await make_get_request(f'persons/{query_data}')

    assert response['status'] == http.HTTPStatus.NOT_FOUND
    assert response['body'] == {"detail":"person not found"}


@pytest.mark.asyncio(scope='session')
async def test_person_search(make_get_request, redis_client):
    cache_key = 'persons:query:lucas'
    await redis_client.delete(cache_key)

    query_data = {"query": "Lucas"}
    response = await make_get_request(f'persons/search/', query_data)
    
    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 4


@pytest.mark.asyncio(scope='session')
async def test_person_search_n_size(make_get_request, redis_client):
    cache_key = 'persons:query:lucas'
    await redis_client.delete(cache_key)

    query_data = {"query": "Lucas", "page": 2, "size": 2}
    response = await make_get_request(f'persons/search/', query_data)

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 2


@pytest.mark.asyncio(scope='session')
async def test_person_n_size_cache(make_get_request, redis_client):
    cache_key = 'persons:query:michael'
    await redis_client.delete(cache_key)

    query_data = {"query": "Michael", "page": 1, "size": 5}
    response = await make_get_request(f'persons/search/', query_data)

    cache = await redis_client.get(cache_key)
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache


@pytest.mark.asyncio(scope='session')
async def test_person_film_list(make_get_request):
    query_data = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'
    response = await make_get_request(f'persons/{query_data}/film')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 46
