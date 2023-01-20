import os

import redis

from url_counter.config import Config

DATABASE_DRIVER = "redis"


def get_redis_url(environment=os.getenv("ENVIRONMENT", "Development")) -> str:
    config = Config.factory(environment)
    return f"{DATABASE_DRIVER}://{config.REDIS_HOST}:{config.REDIS_PORT}"


redis_client = redis.from_url(get_redis_url())
