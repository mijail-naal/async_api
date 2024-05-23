import json
import pytest
import http
import sys

#sys.path.append('..')

import uuid

from testdata.docs.movies import MOVIES


SCHEMA = 'testdata/schemas/movieIndex.json'


@pytest.mark.asyncio(scope='session')
async def test_film_details(make_get_request, es_write_data, json_data, es_data):
    query_data = 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'

    # index_mapping = json_data(SCHEMA)
    # movies = es_data(MOVIES, 'movies')
    # await es_write_data(movies, 'movies', index_mapping)

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
    #await redis_client.flushall()
    query_data = {"query": "Tours"}
    response = await make_get_request(f'films/search/', query_data)
    #print(response)
    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 1


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
    assert response['body'][0]['imdb_rating'] == 8.7


@pytest.mark.asyncio(scope='session')
async def test_film_list_by_genre(make_get_request):

    query_data = {"genre_id":"3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff", 
                  "sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 10}
    response = await make_get_request(f'films', query_data)

    assert response['status'] == http.HTTPStatus.OK
    assert response['body'][0]['imdb_rating'] == 8.4

