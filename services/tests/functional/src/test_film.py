import pytest
import http

from testdata.film_data import (
    CHECK_ID,
    ID_NOT_EXISTS,
    SORT_BY_RATING,
    LIST_BY_GENRE
)

@pytest.mark.asyncio(scope='session')
async def test_film_details(make_get_request):
    response = await make_get_request(f'films/{CHECK_ID}')

    assert response['status'] == http.HTTPStatus.OK
    assert len(response['body']) == 8
    assert response['body']['uuid'] == 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'


@pytest.mark.asyncio(scope='session')
async def test_film_not_found(make_get_request):
    response = await make_get_request(f'films/{ID_NOT_EXISTS}')

    assert response['status'] == http.HTTPStatus.NOT_FOUND
    assert response['body'] == {"detail":"film not found"}


@pytest.mark.asyncio(scope='session')
async def test_film_list(make_get_request):
    response = await make_get_request(f'films', SORT_BY_RATING)
    
    assert response['status'] == http.HTTPStatus.OK
    assert response['body'][0]['imdb_rating'] == 9.6


@pytest.mark.asyncio(scope='session')
async def test_film_list_by_genre(make_get_request):
    response = await make_get_request(f'films', LIST_BY_GENRE)
    
    assert response['status'] == http.HTTPStatus.OK
    assert response['body'][0]['imdb_rating'] == 8.6
