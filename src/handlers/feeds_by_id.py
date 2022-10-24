import os
from typing import Any, Dict

import boto3
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_xray_sdk.core import patch_all

from src.providers.cache.dynamodb import CacheProvider
from src.providers.config.dynamodb import ConfigProvider
from src.providers.fetch.requests import FetchProvider
from src.usecases.html2feed import generate_feed_by_id

patch_all()

logger = Logger()
dynamodb = boto3.resource("dynamodb")
feed_item_table = dynamodb.Table(os.environ["FEED_ITEM_TABLE"])
cache_provider = CacheProvider(table=feed_item_table)
fetch_provider = FetchProvider()
feeds_config_table = dynamodb.Table(os.environ["FEED_CONFIG_TABLE"])
config_provider = ConfigProvider(table=feeds_config_table)


@logger.inject_lambda_context(log_event=True)
def main(event: APIGatewayProxyEvent, context: LambdaContext) -> Dict[str, Any]:
    paths = event["pathParameters"]

    feed_id = paths["feed_id"]
    return {
        "statusCode": 200,
        "body": generate_feed_by_id(
            feed_id=feed_id,
            cache_provider=cache_provider,
            fetch_provider=fetch_provider,
            config_provider=config_provider,
        ),
    }
