from typing import Dict, Protocol


class UrlCounterRepository(Protocol):
    def increment(self, url: str) -> None:
        ...

    def stats(self, limit: int = 10) -> dict[str, int]:
        ...


class InMemoryUrlCounterRepository:
    def __init__(self) -> None:
        self._counts: Dict[str, int] = {}

    def increment(self, url: str) -> None:
        self._counts[url] = self._counts.get(url, 0) + 1

    def stats(self, limit: int = 10) -> Dict[str, int]:
        return dict(sorted(self._counts.items(), key=lambda item: item[1], reverse=True)[:limit])
