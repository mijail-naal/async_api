PATH = 'fixtures'

pytest_plugins = [
    f'{PATH}.es_fixtures',
    f'{PATH}.redis_fixtures',
    f'{PATH}.request_fixtures'
]