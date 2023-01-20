from typing import Tuple

from flask import Blueprint, Response, jsonify

from url_counter.infra.redis.connection import redis_client
from url_counter.infra.redis.repositories.url_counter import RedisUrlCounterRepository
from url_counter.use_cases.generate_url import GenerateUrlUseCase
from url_counter.use_cases.url_counter import UrlCounterUseCase

tests = Blueprint("tests", __name__, url_prefix="/")


@tests.route("/test/<int:number_of_requests>", methods=["POST"])
def run_tests(number_of_requests: int) -> Tuple[Response, int]:
    repository = RedisUrlCounterRepository(redis_client)
    url_counter_use_case = UrlCounterUseCase(repository)
    use_case = GenerateUrlUseCase(url_counter_use_case)
    use_case.execute(number_of_requests)
    return jsonify({"message": "Tests executed successfully"}), 200
