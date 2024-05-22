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


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'query': 'Star'}, {'status': 200, 'length': 20}),
        ({'query': ''}, {'status': 404, 'length': 1}),
        ({'query': 456}, {'status': 404, 'length': 1})
    ]
)
@pytest.mark.asyncio(scope='session')
async def test_film_search(make_get_request, query_data, expected_answer):
    response = await make_get_request(f'films/search/', query_data)

    assert expected_answer['status'] == response['status']
    assert expected_answer['length'] == len(response['body'])


@pytest.mark.asyncio(scope='session')
async def test_film_search(make_get_request):
    page = 1
    size = 20
    query = 'Star'
    response = await make_get_request(f'films/search/?query={query}&page={page}&size={size}')

    assert response['status'] == 200
    assert len(response['body']) == 20