from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

JST = timezone(timedelta(hours=+9), "JST")


class FeedItem:
    def __init__(
        self,
        url: str,
        title: str,
        updated_at: datetime,
        expired_at: datetime,
    ):
        self.url = url
        self.title = title
        self.updated_at = updated_at
        self.expired_at = expired_at


class FeedConfig:
    def __init__(
        self,
        url: str,
        query: str,
        title_query: str,
        title_attr: str,
        link_query: str,
        link_attr: str,
        feed_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
    ):
        self.url = url
        self.query = query
        self.title_query = title_query
        self.title_attr = title_attr
        self.link_query = link_query
        self.link_attr = link_attr

        if feed_id is None:
            self.feed_id = uuid4()
        else:
            self.feed_id = feed_id
        if created_at is None:
            self.created_at = datetime.now(JST)
        else:
            self.created_at = created_at
