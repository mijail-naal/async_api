import os
import time
import backoff

from elasticsearch import (
    Elasticsearch,
    ConnectionError,
    NotFoundError,
    RequestError
)

from utils.helpers import logger

timeout = time.time() + 60 * 5

ELASTIC_PROTOCOL = os.getenv('ELASTIC_PROTOCOL', 'http')
ELASTIC_HOST = os.getenv('ELASTIC_HOST', '127.0.0.1')
ELASTIC_PORT = int(os.getenv('ELASTIC_PORT', 9200))

hosts = [f'{ELASTIC_PROTOCOL}://{ELASTIC_HOST}:{ELASTIC_PORT}']


@backoff.on_exception(
    backoff.expo,
    (ConnectionError, NotFoundError, RequestError),
    max_time=60
)
def connect_to_es(es: Elasticsearch) -> None:
    if not es.ping():
        raise ConnectionError("Failed to connect")

    logger.info('Successfully connected to Elasticsearch')


if __name__ == '__main__':
    es_client = Elasticsearch(hosts=hosts, validate_cert=False, use_ssl=False)
    connect_to_es(es_client)
