import json
import pytest
import http

from testdata.person_data import (
    CHECK_ID,
    ID_NOT_EXISTS,
    PERSON_CACHE,
    PERSON_LIST,
    PERSON_BY_PAGE_SIZE,
    PERSON_UUID
)


@pytest.mark.asyncio(scope='session')
async def test_person_details(make_get_request):
    response = await make_get_request(f'persons/{CHECK_ID}')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 3
    assert response['body']['uuid'] == CHECK_ID


@pytest.mark.asyncio(scope='session')
async def test_person_not_found(make_get_request):
    response = await make_get_request(f'persons/{ID_NOT_EXISTS}')

    assert response['status'] == http.HTTPStatus.NOT_FOUND
    assert response['body'] == {"detail":"person not found"}


@pytest.mark.asyncio(scope='session')
async def test_person_search(make_get_request, redis_client):
    await redis_client.delete(PERSON_CACHE[0])
    response = await make_get_request(f'persons/search/', PERSON_LIST)
    
    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 4


@pytest.mark.asyncio(scope='session')
async def test_person_search_n_size(make_get_request, redis_client):
    await redis_client.delete(PERSON_CACHE[0])
    response = await make_get_request(f'persons/search/', PERSON_BY_PAGE_SIZE[0])

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 2


@pytest.mark.asyncio(scope='session')
async def test_person_n_size_cache(make_get_request, redis_client):
    await redis_client.delete(PERSON_CACHE[1])
    response = await make_get_request(f'persons/search/', PERSON_BY_PAGE_SIZE[1])

    cache = await redis_client.get(PERSON_CACHE[1])
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache


@pytest.mark.asyncio(scope='session')
async def test_person_film_list(make_get_request):
    response = await make_get_request(f'persons/{PERSON_UUID}/film')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 46
