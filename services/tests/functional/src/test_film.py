import pytest


@pytest.mark.asyncio(scope='session')
async def test_film_details(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'
    response = await make_get_request(f'films/{query_data}')

    assert response['status'] == 200
    assert len(response['body']) == 8
    assert response['body']['uuid'] == 'a1bf30bf-08ee-4000-8d9a-a1e17ab2c197'


@pytest.mark.asyncio(scope='session')
async def test_film_not_found(make_get_request):
    query_data = 'a1bf30bf-08ee-4000-@-¿+-no-exists-id'
    response = await make_get_request(f'films/{query_data}')

    assert response['status'] == 404
    assert response['body'] == {"detail":"film not found"}


@pytest.mark.asyncio(scope='session')
async def test_film_list(make_get_request):

    query_data = {"sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 2}
    response = await make_get_request(f'films', query_data)

    assert response['status'] == 200
    assert response['body'][0]['imdb_rating'] == 9.6


@pytest.mark.asyncio(scope='session')
async def test_film_list_by_genre(make_get_request):

    query_data = {"genre_id":"ca88141b-a6b4-450d-bbc3-efa940e4953f", 
                  "sort_field": "imdb_rating", "sort_order":"desc", "page": 1, "size": 10}
    response = await make_get_request(f'films', query_data)

    assert response['status'] == 200
    assert response['body'][0]['imdb_rating'] == 8.6
