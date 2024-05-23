import sys
import backoff

from elasticsearch import Elasticsearch
from logger import logger

sys.path.append("..")

from settings import test_settings


def backoff_handler(details: dict) -> None:
    """Backoff event handler logging function"""
    logger.warning(
        "Backing off {wait:0.1f} seconds after {tries} tries "
        "calling function {target.__name__} with args {args}"
        .format(**details)
    )


@backoff.on_exception(backoff.expo,
                      ConnectionError,
                      on_backoff=backoff_handler)
def es_connection(client: Elasticsearch):
    if not client.ping():
        logger.info("Trying to connect ...")
        raise ConnectionError("Failed to connect")
    
    logger.info("connected.")


if __name__ == '__main__':
    es_client = Elasticsearch(
        hosts=test_settings.es_host, 
        verify_certs=False,
        max_retries=0,
        # retry_on_status=0,
        # retry_on_timeout=False,
    )
    
    es_connection(es_client)