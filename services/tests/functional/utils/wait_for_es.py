import time
import backoff

from elasticsearch import (
    Elasticsearch,
    ConnectionError,
    NotFoundError,
    RequestError
)

from ..settings import settings
from helpers import logger

timeout = time.time() + 60 * 5
hosts = [f'{settings.elastic_protocol}://{settings.elastic_host}:{settings.elastic_port}']


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
