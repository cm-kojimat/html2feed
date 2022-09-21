from datetime import datetime, timedelta, timezone
from functools import lru_cache
from math import floor

from mypy_boto3_dynamodb.service_resource import Table

from src.domains.cache_provider import CacheProvider as CacheProviderInterface
from src.domains.feed import FeedItem

JST = timezone(timedelta(hours=+9), "JST")


class CacheProvider(CacheProviderInterface):
    def __init__(self, table: Table):
        self.table = table

    @lru_cache(maxsize=512)
    def fetch_feed_item(self, url: str, title: str) -> FeedItem:
        resp = self.table.get_item(Key={"url": url})

        if "Item" in resp and "updated_at" in resp["Item"]:
            item = resp["Item"]
            return FeedItem(
                url=item["url"],
                title=item["title"],
                updated_at=datetime.fromtimestamp(int(item["updated_at"]), tz=JST),
                expired_at=datetime.fromtimestamp(int(item["expired_at"]), tz=JST),
            )

        feed = FeedItem(
            url=url,
            title=title,
            updated_at=datetime.now(JST),
            expired_at=datetime.now(JST) + timedelta(days=30 * 6),
        )
        self.table.put_item(
            Item={
                "url": feed.url,
                "title": feed.title,
                "updated_at": floor(feed.updated_at.timestamp()),
                "expired_at": floor(feed.expired_at.timestamp()),
            }
        )
        return feed
