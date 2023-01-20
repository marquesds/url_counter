import pytest
from flask import Flask
from flask.testing import FlaskClient

from url_counter import create_app
from url_counter.infra.redis.connection import redis_client


class TestApiV1:
    @pytest.fixture()
    def app(self) -> None:
        app = create_app("Testing")

        yield app
        redis_client.flushdb()

    @pytest.fixture()
    def client(self, app: Flask) -> FlaskClient:
        return app.test_client()

    def test_should_increment_url(self, client: FlaskClient) -> None:
        response = client.get("/api/")
        assert response.status_code == 201
        assert response.json == {"url": "/api/", "count": 1}

        response = client.get("/api/")
        assert response.status_code == 201
        assert response.json == {"url": "/api/", "count": 2}

        response = client.get("/api/other")
        assert response.status_code == 201
        assert response.json == {"url": "/api/other", "count": 1}

        response = client.get("/api/other")
        assert response.status_code == 201
        assert response.json == {"url": "/api/other", "count": 2}

        response = client.get("/api/other")
        assert response.status_code == 201
        assert response.json == {"url": "/api/other", "count": 3}

        response = client.get("/api/")
        assert response.status_code == 201
        assert response.json == {"url": "/api/", "count": 3}

    def test_should_not_increment_invalid_url(self, client: FlaskClient) -> None:
        url = "/api/awesome/url/with/too/many/paths/1"
        response = client.get(url)
        assert response.status_code == 400
        assert response.json == {"error": f"Error incrementing url: Invalid URL: {url}"}
