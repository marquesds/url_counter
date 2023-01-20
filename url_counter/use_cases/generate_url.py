import random
import string
from typing import Iterator

from url_counter.use_cases.url_counter import UrlCounterUseCase


class GenerateUrlUseCase:
    def __init__(self, url_counter_use_case: UrlCounterUseCase):
        self.url_counter_use_case = url_counter_use_case

    def execute(self, request_number: int) -> None:
        for url in self.generate_urls(request_number):
            self.url_counter_use_case.increment(url)

    def generate_urls(self, request_number: int) -> Iterator[str]:
        return iter([self.generate_url() for i in range(request_number)])

    def generate_url(self, path_size_limit: int = 6) -> str:
        path_size = random.randint(1, path_size_limit)
        return "/".join(self.generate_random_string(path_size_limit) for i in range(path_size))

    def generate_random_string(self, size_limit: int = 10) -> str:
        string_size = random.randint(1, size_limit)
        return "".join(random.choice(string.ascii_letters) for i in range(string_size))
