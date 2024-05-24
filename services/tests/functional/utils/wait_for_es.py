import time
import backoff

from elasticsearch import (
    Elasticsearch,
    ConnectionError,
    NotFoundError,
    RequestError
)

from logger import logger
from settings import test_settings


timeout = time.time() + 60 * 5
hosts = [f'{test_settings.elastic_protocol}://{test_settings.elastic_host}:{test_settings.elastic_port}']


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
    es_client = Elasticsearch(hosts=hosts, verify_certs=False)
    connect_to_es(es_client)
