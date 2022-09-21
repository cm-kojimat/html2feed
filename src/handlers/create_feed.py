import json
import os
from base64 import b64decode
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

import boto3
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_xray_sdk.core import patch_all

from src.domains.feed import FeedConfig
from src.providers.config.dynamodb import ConfigProvider
from src.usecases.html2feed import create_feed_config

patch_all()

logger = Logger()
dynamodb = boto3.resource("dynamodb")
feeds_config_table = dynamodb.Table(os.environ["FEED_CONFIG_TABLE"])
config_provider = ConfigProvider(table=feeds_config_table)


@logger.inject_lambda_context(log_event=True)
def main(event: APIGatewayProxyEvent, context: LambdaContext) -> Dict[str, Any]:
    body = b64decode(event["body"]).decode("utf-8")
    params = json.loads(body)

    config = create_feed_config(
        config=FeedConfig(
            url=params["url"],
            query=params["query"],
            title_query=params["title_query"],
            title_attr=params.get("title_attr", "text"),
            link_query=params["link_query"],
            link_attr=params.get("link_attr", "href"),
        ),
        config_provider=config_provider,
    )

    return {
        "statusCode": 200,
        "body": json.dumps(config.__dict__, default=json_serial),
    }


def json_serial(obj):
    if isinstance(obj, FeedConfig):
        return obj.__dict__
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError(f"Type {type(obj)} not serializable")
