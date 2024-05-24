import json
import pytest
import http

from testdata.genre_data import (
    CHECK_ID,
    ID_NOT_EXISTS,
    GENRE_CACHE
)


@pytest.mark.asyncio(scope='session')
async def test_genre_details(make_get_request):
    response = await make_get_request(f'genres/{CHECK_ID}')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 2
    assert response['body']['name'] == 'Action'
    assert response['body']['uuid'] == CHECK_ID


@pytest.mark.asyncio(scope='session')
async def test_genre_not_found(make_get_request):
    response = await make_get_request(f'genre/{ID_NOT_EXISTS}')

    assert response['status'] == http.HTTPStatus.NOT_FOUND
    assert response['body'] == {"detail":"Not Found"}


@pytest.mark.asyncio(scope='session')
async def test_genre_list(make_get_request):
    response = await make_get_request(f'genres')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 26


@pytest.mark.asyncio(scope='session')
async def test_genre_cache(make_get_request, redis_client):
    await redis_client.delete(GENRE_CACHE)
    response = await make_get_request(f'genres')

    cache = await redis_client.get(GENRE_CACHE)
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache

