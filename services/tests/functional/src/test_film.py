import http
import json
import pytest


@pytest.mark.asyncio(scope='session')
async def test_film_details(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'
    response = await make_get_request(f'films/{query_data}')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 8
    assert response['body']['uuid'] == 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'


@pytest.mark.asyncio(scope='session')
async def test_film_not_found(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-@-¿+-no-exists-id'
    response = await make_get_request(f'films/{query_data}')

    assert response['status'] == http.HTTPStatus.NOT_FOUND
    assert response['body'] == {"detail":"film not found"}


@pytest.mark.asyncio(scope='session')
async def test_film_search(make_get_request):
    query_data = {"query": "Wars"}
    response = await make_get_request(f'films/search/', query_data)

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 10


@pytest.mark.asyncio(scope='session')
async def test_film_search_n_size(make_get_request, redis_client):
    cache_key = 'film:query:star'
    await redis_client.delete(cache_key)

    query_data = {"query": "Star", "page": 1, "size": 5}
    response = await make_get_request(f'films/search/', query_data)

    assert response['status'] == http.HTTPStatus.OK
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


@pytest.mark.asyncio(scope='session')
async def test_film_list(make_get_request):

    query_data = {"sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 2}
    response = await make_get_request(f'films', query_data)

    assert response['status'] == http.HTTPStatus.OK
    assert response['body'][0]['imdb_rating'] == 9.6


@pytest.mark.asyncio(scope='session')
async def test_film_list_by_genre(make_get_request):

    query_data = {"genre_id":"ca88141b-a6b4-450d-bbc3-efa940e4953f", 
                  "sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 10}
    response = await make_get_request(f'films', query_data)

    assert response['status'] == http.HTTPStatus.OK
    assert response['body'][0]['imdb_rating'] == 8.6
