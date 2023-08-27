import boto3
import botocore
from app.settings import settings

# For a Boto3 client.

if settings.environment == "local":
    dynamodb = boto3.client(
        "dynamodb",
        endpoint_url="http://127.0.0.1:8000",
        region_name=settings.aws_region_name,
    )
else:
    dynamodb = boto3.client(
        "dynamodb",
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region_name,
    )


async def put_item(partition_key: str, sort_key: str, value: str) -> None:
    dynamodb.put_item(
        TableName="data",
        Item={
            "PK": {"S": partition_key},
            "SK": {"S": sort_key},
            "VALUE": {"S": value},
        },
    )


async def get_item(partition_key: str, sort_key: str) -> str | None:
    try:
        response = dynamodb.get_item(
            TableName="data",
            Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        )
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            return
    return response["Item"]["VALUE"]["S"]


async def delete_item(partition_key: str, sort_key) -> bool:
    response = dynamodb.delete_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        ReturnValues="ALL_OLD",
    )

    # The "delete_item" operation is idempotent.
    # This is a trick to check if an item is deleted or not
    return "Attributes" in response
