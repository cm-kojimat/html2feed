from uuid import UUID

from src.domains.feed import FeedConfig


class ConfigProvider:
    def get(self, id: UUID) -> FeedConfig:
        raise Exception("failed to unimprements method")

    def create(self, config: FeedConfig) -> FeedConfig:
        raise Exception("failed to unimprements method")
