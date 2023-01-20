import pytest
from flask import Flask
from flask.testing import FlaskClient

from url_counter import create_app
from url_counter.infra.redis.connection import redis_client


class TestTests:
    @pytest.fixture()
    def app(self) -> None:
        app = create_app("Testing")

        yield app
        redis_client.flushdb()

    @pytest.fixture()
    def client(self, app: Flask) -> FlaskClient:
        return app.test_client()

    def test_should_run_tests(self, client: FlaskClient) -> None:
        response = client.post("/test/5")
        assert response.status_code == 200
        assert response.json == {"message": "Tests executed successfully"}
