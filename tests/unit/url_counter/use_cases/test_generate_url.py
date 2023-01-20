import pytest

from url_counter.repositories.url_counter import InMemoryUrlCounterRepository
from url_counter.use_cases.generate_url import GenerateUrlUseCase
from url_counter.use_cases.url_counter import UrlCounterUseCase


class TestGenerateUrlUseCase:
    @pytest.fixture(autouse=True)
    def use_case(self) -> GenerateUrlUseCase:
        repository = InMemoryUrlCounterRepository()
        url_counter_use_case = UrlCounterUseCase(repository)
        return GenerateUrlUseCase(url_counter_use_case)

    def test_should_generate_urls_and_increment(self, use_case: GenerateUrlUseCase) -> None:
        use_case.execute(10)
        result = use_case.url_counter_use_case.stats()
        assert result.keys() is not None

    def test_should_generate_urls(self, use_case: GenerateUrlUseCase) -> None:
        result = use_case.generate_urls(10)
        assert len(list(result)) == 10

    def test_should_generate_url(self, use_case: GenerateUrlUseCase) -> None:
        result = use_case.generate_url()
        assert len(result) > 0

    def test_should_generate_random_string(self, use_case: GenerateUrlUseCase) -> None:
        result = use_case.generate_random_string()
        assert len(result) > 0
