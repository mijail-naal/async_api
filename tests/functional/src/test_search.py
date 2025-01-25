import pytest
import json
import http

from testdata.search_data import (
    FILM_SEARCH_BY_WORD,
    FILM_CACHE,
    SEARCH_PAGE_SIZE
)


@pytest.mark.asyncio(scope='session')
async def test_film_search(make_get_request):
    response = await make_get_request(f'films/search/', FILM_SEARCH_BY_WORD)

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 10


@pytest.mark.asyncio(scope='session')
async def test_film_search_n_size(make_get_request, redis_client):
    await redis_client.delete(FILM_CACHE)
    response = await make_get_request(f'films/search/', SEARCH_PAGE_SIZE[0])

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 5


@pytest.mark.asyncio(scope='session')
async def test_film_search_n_size_cache(make_get_request, redis_client):
    await redis_client.delete(FILM_CACHE)
    response = await make_get_request(f'films/search/', SEARCH_PAGE_SIZE[1])

    cache = await redis_client.get(FILM_CACHE)
    cache = json.loads(cache)

    assert len(response['body']) == len(cache)
    assert response['body'] == cache
