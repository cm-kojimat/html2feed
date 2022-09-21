import requests

from src.domains.fetch_provider import FetchProvider as FetchProviderInterface


class FetchProvider(FetchProviderInterface):
    def fetch(self, url: str) -> bytes:
        resp = requests.get(url, timeout=300)
        return resp.content
