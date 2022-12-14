from functools import reduce
from typing import Dict, Tuple
from urllib.parse import urlparse
from uuid import UUID

from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

from src.domains.cache_provider import CacheProvider
from src.domains.config_provider import ConfigProvider
from src.domains.feed import FeedConfig
from src.domains.fetch_provider import FetchProvider
from src.domains.selector import AttrSelector, EntrySelector


def _href2link(uobj, href: str) -> str:
    if href.startswith("http://") or href.startswith("https://"):
        return href

    if href.startswith("/"):
        return f"{uobj.scheme}://{uobj.netloc}{href}"

    return f"{uobj.geturl()}{href}"


def _list2uniq(acc: Dict[str, str], elem: Tuple[str, str]):
    acc[elem[0]] = elem[1]
    return acc


def generate_feed(
    url: str,
    selector: EntrySelector,
    cache_provider: CacheProvider,
    fetch_provider: FetchProvider,
    content_type: str = "atom",
) -> str:
    uobj = urlparse(url)

    soup = BeautifulSoup(fetch_provider.fetch(url), "lxml")

    feed_gen = FeedGenerator()
    feed_gen.id(url)
    if soup.title is not None:
        text = soup.title.text
        feed_gen.title(text)
        feed_gen.description(text)
    feed_gen.link(href=url)

    link_elements = selector.select(soup)
    feeds = [
        cache_provider.fetch_feed_item(url=_href2link(uobj, href=href), title=title)
        for href, title in reduce(_list2uniq, link_elements, {}).items()
    ]
    for feed in sorted(
        feeds,
        key=lambda feed: feed.updated_at,
        reverse=True,
    ):
        entry = feed_gen.add_entry()
        entry.id(feed.url)
        entry.title(feed.title)
        entry.link(href=feed.url)
        entry.updated(feed.updated_at)

    if content_type == "atom":
        return feed_gen.atom_str(pretty=True)

    return feed_gen.rss_str(pretty=True)


def generate_feed_by_id(
    feed_id: UUID,
    cache_provider: CacheProvider,
    fetch_provider: FetchProvider,
    config_provider: ConfigProvider,
    content_type: str = "atom",
):
    config = config_provider.get(feed_id)
    return generate_feed(
        url=config.url,
        selector=EntrySelector(
            query=config.query,
            title=AttrSelector(query=config.title_query, attr=config.title_attr),
            link=AttrSelector(query=config.link_query, attr=config.link_attr),
        ),
        cache_provider=cache_provider,
        fetch_provider=fetch_provider,
        content_type=content_type,
    )


def create_feed_config(
    config: FeedConfig, config_provider: ConfigProvider
) -> FeedConfig:
    return config_provider.create(config)
