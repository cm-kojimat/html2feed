from urllib.request import urlopen

from src.domains.fetch_provider import FetchProvider as FetchProviderInterface


class FetchProvider(FetchProviderInterface):
    def fetch(self, url: str) -> bytes:
        with urlopen(url) as resp:
            return resp.content
