import logging
from typing import Tuple

from flask import Blueprint, Response, jsonify

from url_counter.infra.redis.connection import redis_client
from url_counter.infra.redis.repositories.url_counter import RedisUrlCounterRepository
from url_counter.use_cases.url_counter import UrlCounterUseCase

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/")

logger = logging.getLogger(__name__)


@api_v1.route("/", defaults={"custom_path": ""})
@api_v1.route("/<path:custom_path>")
def increment_url(custom_path: str) -> Tuple[Response, int]:
    repository = RedisUrlCounterRepository(redis_client)
    use_case = UrlCounterUseCase(repository)
    full_path = f"/api/{custom_path}"
    try:
        use_case.increment(full_path)
    except ValueError as e:
        error_message = f"Error incrementing url: {str(e)}"
        logger.error(error_message)
        return jsonify({"error": error_message}), 400

    return jsonify({"url": full_path, "count": use_case.stats()[full_path]}), 201
