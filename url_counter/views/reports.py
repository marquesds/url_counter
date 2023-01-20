from typing import Tuple

from flask import Blueprint, Response, jsonify

from url_counter.infra.redis.connection import redis_client
from url_counter.infra.redis.repositories.url_counter import RedisUrlCounterRepository
from url_counter.use_cases.url_counter import UrlCounterUseCase

reports = Blueprint("reports", __name__, url_prefix="/")


@reports.route("/stats")
def generate_report() -> Tuple[Response, int]:
    repository = RedisUrlCounterRepository(redis_client)
    use_case = UrlCounterUseCase(repository)
    return jsonify(use_case.stats()), 200
