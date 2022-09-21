from typing import Iterable, Optional, Tuple

from bs4 import Tag


class AttrSelector:
    def __init__(self, query: str, attr: str = "text"):
        self.query = query
        self.attr = attr

    def select_one(self, item: Tag) -> Optional[str]:
        target = item.select_one(self.query)

        if target is None:
            return None

        if self.attr == "text":
            return target.text

        return target.attrs[self.attr]


class EntrySelector:
    def __init__(self, query: str, title: AttrSelector, link: AttrSelector):
        self.query = query
        self.title = title
        self.link = link

    def select(self, item: Tag) -> Iterable[Tuple[str, str]]:
        for target in item.select(self.query):
            if target is None:
                continue

            link = self.link.select_one(target)
            title = self.title.select_one(target)

            if link is None or title is None:
                continue

            yield (link, title)
