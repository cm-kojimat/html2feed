from src.domains.feed import FeedItem


class CacheProvider:
    def fetch_feed_item(self, url: str, title: str) -> FeedItem:
        raise Exception("failed to unimprements method")
