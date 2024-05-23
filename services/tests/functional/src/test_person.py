import json
import pytest

from testdata.docs.persons import PERSONS


SCHEMA = 'testdata/schemas/personIndex.json'


# @pytest.mark.asyncio(scope='session')
# async def test_create_index(es_write_data, json_data, es_data):
#     index_mapping = json_data(SCHEMA)
#     movies = es_data(PERSONS, 'persons')
#     await es_write_data(movies, 'persons', index_mapping)


@pytest.mark.asyncio(scope='session')
async def test_person_details(make_get_request):
    query_data = '58ed700d-4e64-49cd-a89f-b858d9bd399c'
    response = await make_get_request(f'persons/{query_data}')

    assert response['status'] == 200
    assert len(response['body']) == 3
    assert response['body']['uuid'] == query_data


@pytest.mark.asyncio(scope='session')
async def test_person_not_found(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-@-¿+-no-exists-id'
    response = await make_get_request(f'persons/{query_data}')

    assert response['status'] == 404
    assert response['body'] == {"detail":"person not found"}


@pytest.mark.asyncio(scope='session')
async def test_person_search(make_get_request, redis_client):
    cache_key = 'persons:query:rasmus'
    await redis_client.delete(cache_key)

    query_data = {"query": "Rasmus"}
    response = await make_get_request(f'persons/search/', query_data)
    #print(response)
    assert response['status'] == 200
    assert len(response['body']) == 1


@pytest.mark.asyncio(scope='session')
async def test_person_search_n_size(make_get_request, redis_client):
    cache_key = 'persons:query:rasmus'
    await redis_client.delete(cache_key)

    query_data = {"query": "Rasmus", "page": 1, "size": 2}
    response = await make_get_request(f'persons/search/', query_data)

    assert response['status'] == 200
    assert len(response['body']) == 1


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


# @pytest.mark.asyncio(scope='session')
# async def test_person_film_list(make_get_request):

#     #query_data = {"sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 2}
#     query_data = '08b369d9-5448-4def-83e3-33bde45cf261'
#     response = await make_get_request(f'persons/{query_data}/film')

#     assert response['status'] == 200
#     assert len(response['body']) == 46
