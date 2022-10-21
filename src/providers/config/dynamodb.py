from datetime import datetime, timedelta, timezone
from math import floor
from uuid import UUID

from mypy_boto3_dynamodb.service_resource import Table

from src.domains.config_provider import ConfigProvider as ConfigProviderInterface
from src.domains.feed import FeedConfig

JST = timezone(timedelta(hours=+9), "JST")


class ConfigProvider(ConfigProviderInterface):
    def __init__(self, table: Table):
        self.table = table

    def get(self, feed_id: UUID) -> FeedConfig:
        resp = self.table.get_item(Key={"id": str(feed_id)})
        item = resp["Item"]
        return FeedConfig(
            feed_id=feed_id,
            url=item["url"],
            query=item["query"],
            title_query=item["title_query"],
            title_attr=item["title_attr"],
            link_query=item["link_query"],
            link_attr=item["link_attr"],
            created_at=datetime.fromtimestamp(int(item["created_at"]), tz=JST),
        )

    def create(self, config: FeedConfig):
        self.table.put_item(
            Item={
                "id": str(config.feed_id),
                "url": config.url,
                "query": config.query,
                "title_query": config.title_query,
                "title_attr": config.title_attr,
                "link_query": config.link_query,
                "link_attr": config.link_attr,
                "created_at": floor(config.created_at.timestamp()),
            }
        )
        return config
