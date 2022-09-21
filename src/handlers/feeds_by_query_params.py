import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_xray_sdk.core import patch_all

from src.domains.selector import AttrSelector, EntrySelector
from src.providers.cache.dynamodb import CacheProvider
from src.providers.fetch.requests import FetchProvider
from src.usecases.html2feed import generate_feed

patch_all()

logger = Logger()
dynamodb = boto3.resource("dynamodb")
feed_item_table = dynamodb.Table(os.environ["FEED_ITEM_TABLE"])
cache_provider = CacheProvider(table=feed_item_table)
fetch_provider = FetchProvider()


@logger.inject_lambda_context(log_event=True)
def main(event: APIGatewayProxyEvent, context: LambdaContext) -> Dict[str, Any]:
    params = event.get("queryStringParameters")

    return {
        "statusCode": 200,
        "body": generate_feed(
            url=params["url"],
            selector=EntrySelector(
                query=params["query"],
                title=AttrSelector(
                    query=params["title_query"],
                    attr=params.get("title_attr", "text"),
                ),
                link=AttrSelector(
                    query=params["link_query"], attr=params.get("link_attr", "href")
                ),
            ),
            fetch_provider=fetch_provider,
            cache_provider=cache_provider,
        ),
    }
