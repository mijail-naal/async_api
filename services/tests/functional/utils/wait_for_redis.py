import os
import time
import backoff

from redis import Redis
from utils.helpers import logger

timeout = time.time() + 60 * 5

REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

redis = Redis(host=REDIS_HOST, port=REDIS_PORT)


@backoff.on_exception(
    backoff.expo,
    Exception,
    max_time=60
)
def connect(redis: Redis) -> None:
    redis.ping()
    logger.info('Successfully connected to Redis')


if __name__ == "__main__":
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    connect(redis)
