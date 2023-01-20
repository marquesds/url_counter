from redis.client import Redis

from url_counter.repositories.url_counter import UrlCounterRepository


class RedisUrlCounterRepository(UrlCounterRepository):
    def __init__(self, redis_client: Redis) -> None:
        self.redis_client = redis_client
        self.set_name = "url"

    def increment(self, url) -> None:
        self.redis_client.zadd(self.set_name, {url: 1}, incr=True)

    def stats(self, limit: int = 10) -> dict[str, int]:
        return dict(
            [
                (key.decode(), int(value))
                for key, value in self.redis_client.zrange(self.set_name, 0, limit - 1, withscores=True)
            ]
        )
