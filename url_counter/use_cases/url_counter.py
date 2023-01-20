from url_counter.repositories.url_counter import UrlCounterRepository


class UrlCounterUseCase:
    def __init__(self, repository: UrlCounterRepository):
        self.repository = repository

    def increment(self, url: str) -> None:
        if not self.valid_url(url):
            raise ValueError(f"Invalid URL: {url}")
        self.repository.increment(url)

    def stats(self, limit: int = 10) -> dict[str, int]:
        return self.repository.stats(limit)

    def valid_url(self, url: str) -> bool:
        return len(url.split("/")) < 8
