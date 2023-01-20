import pytest

from url_counter.infra.redis.connection import redis_client
from url_counter.infra.redis.repositories.url_counter import RedisUrlCounterRepository


class TestRedisUrlCounterRepository:
    @pytest.fixture(autouse=True)
    def flush_redis(self) -> None:
        redis_client.flushdb()

    @pytest.fixture(autouse=True)
    def repository(self) -> RedisUrlCounterRepository:
        return RedisUrlCounterRepository(redis_client)

    def test_should_increment_a_hit_for_new_url(self, repository: RedisUrlCounterRepository) -> None:
        url = "/awesome/url"
        repository.increment(url)
        repository.increment(url)

        result = repository.stats()
        assert result[url] == 2

    def test_should_rank_urls_by_hits(self, repository: RedisUrlCounterRepository) -> None:
        url_1 = "/awesome/url"
        url_2 = "/awesome/url/2"
        url_3 = "/awesome/url/3"
        repository.increment(url_1)
        repository.increment(url_2)
        repository.increment(url_3)
        repository.increment(url_1)
        repository.increment(url_2)
        repository.increment(url_1)

        result = repository.stats()
        assert result == {url_1: 3, url_2: 2, url_3: 1}
