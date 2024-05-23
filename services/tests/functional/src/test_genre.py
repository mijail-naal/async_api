import json
import pytest
import sys

sys.path.append('..')

from testdata.docs.genres import GENRES


SCHEMA = 'testdata/schemas/genreIndex.json'


# @pytest.mark.asyncio(scope='session')
# async def test_create_index(es_write_data, json_data, es_data):
#     index_mapping = json_data(SCHEMA)
#     movies = es_data(GENRES, 'genres')
#     await es_write_data(movies, 'genres', index_mapping)


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

    #query_data = {"sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 2}
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






# @pytest.mark.asyncio(scope='session')
# async def test_film_search(make_get_request):
#     query_data = {"query": "Wars"}
#     response = await make_get_request(f'films/search/', query_data)
#     #print(response)
#     assert response['status'] == 200
#     assert len(response['body']) == 10


# @pytest.mark.asyncio(scope='session')
# async def test_film_search_n_size(make_get_request, redis_client):
#     cache_key = 'film:query:star'
#     await redis_client.delete(cache_key)

#     query_data = {"query": "Star", "page": 1, "size": 5}
#     response = await make_get_request(f'films/search/', query_data)

#     assert response['status'] == 200
#     assert len(response['body']) == 5


# @pytest.mark.asyncio(scope='session')
# async def test_film_list_by_genre(make_get_request):

#     query_data = {"genre_id":"ca88141b-a6b4-450d-bbc3-efa940e4953f", 
#                   "sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 10}
#     response = await make_get_request(f'films', query_data)

#     assert response['status'] == 200
#     assert response['body'][0]['imdb_rating'] == 8.6
