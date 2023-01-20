import pytest

from url_counter.repositories.url_counter import InMemoryUrlCounterRepository
from url_counter.use_cases.url_counter import UrlCounterUseCase


class TestUrlCounterUseCase:
    @pytest.fixture(autouse=True)
    def use_case(self) -> UrlCounterUseCase:
        repository = InMemoryUrlCounterRepository()
        return UrlCounterUseCase(repository)

    def test_should_increment_a_hit_for_new_url(self, use_case: UrlCounterUseCase) -> None:
        url = "/awesome/url"
        use_case.increment(url)
        use_case.increment(url)

        result = use_case.stats()
        assert result[url] == 2

    def test_should_rank_urls_by_hits(self, use_case: UrlCounterUseCase) -> None:
        url_1 = "/awesome/url"
        url_2 = "/awesome/url/2"
        url_3 = "/awesome/url/3"
        use_case.increment(url_1)
        use_case.increment(url_2)
        use_case.increment(url_3)
        use_case.increment(url_1)
        use_case.increment(url_2)
        use_case.increment(url_1)

        result = use_case.stats()
        assert result == {url_1: 3, url_2: 2, url_3: 1}

    def test_should_raise_error_for_invalid_url(self, use_case: UrlCounterUseCase) -> None:
        url = "/awesome/url/with/too/many/paths/1"
        with pytest.raises(ValueError):
            use_case.increment(url)
