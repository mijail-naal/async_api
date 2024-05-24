import time
import backoff

from redis import Redis

from logger import logger
from settings import test_settings

timeout = time.time() + 60 * 5


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_time=60
)
def connect(redis: Redis) -> None:
    redis.ping()
    logger.info('Successfully connected to Redis')


if __name__ == "__main__":
    redis = Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
        decode_responses=True
    )
    connect(redis)
