import sys
import backoff

from redis import Redis
from redis.exceptions import ConnectionError
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
def redis_connection(client: Redis):
    if not client.ping():
        logger.info("Trying to connect ...")
        raise ConnectionError("Failed to connect")
    
    logger.info("connected.")


if __name__ == '__main__':
    redis_client = Redis(
        host=test_settings.redis_host, 
        port=test_settings.redis_port, 
        decode_responses=True
    )
    
    redis_connection(redis_client)