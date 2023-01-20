import pytest
from flask import Flask
from flask.testing import FlaskClient

from url_counter import create_app
from url_counter.infra.redis.connection import redis_client
from url_counter.infra.redis.repositories.url_counter import RedisUrlCounterRepository
from url_counter.use_cases.generate_url import GenerateUrlUseCase
from url_counter.use_cases.url_counter import UrlCounterUseCase


class TestReport:
    @pytest.fixture()
    def app(self) -> None:
        app = create_app("Testing")

        yield app
        redis_client.flushdb()

    @pytest.fixture()
    def client(self, app: Flask) -> FlaskClient:
        return app.test_client()

    def test_should_return_top_urls(self, client: FlaskClient) -> None:
        for i in range(0, 100):
            client.get("/api/")

        for i in range(0, 50):
            client.get("/api/other")

        for i in range(0, 20):
            client.get("/api/other/1")

        for i in range(0, 10):
            client.get("/api/other/2")

        response = client.get("/stats")
        assert response.status_code == 200
        assert response.json == {
            "/api/": 100,
            "/api/other": 50,
            "/api/other/1": 20,
            "/api/other/2": 10,
        }

    def test_should_return_top_urls_with_limit(self, client: FlaskClient) -> None:
        repository = RedisUrlCounterRepository(redis_client)
        url_counter_use_case = UrlCounterUseCase(repository)
        generate_url_use_case = GenerateUrlUseCase(url_counter_use_case)

        generate_url_use_case.execute(100)

        response = client.get("/stats")

        assert response.status_code == 200
        assert len(response.json.keys()) == 10
