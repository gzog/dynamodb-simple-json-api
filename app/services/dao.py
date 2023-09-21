from app.utils.aws import get_dynamodb_client
from botocore import exceptions
from datetime import datetime
from app.settings import settings
from app.exceptions import MaxAllowedSizeExceeded


async def create_or_update(
    partition_key: str, sort_key: str, value: str, ttl: int | None
) -> None:
    item = {"PK": {"S": partition_key}, "SK": {"S": sort_key}, "VALUE": {"S": value}}

    if ttl:
        item["TTL"] = {"N": str(ttl)}

    async with get_dynamodb_client() as dynamodb:
        try:
            await dynamodb.put_item(
                TableName=settings.aws_dynamodb_table_name,
                Item=item,
            )
        except exceptions.ClientError as e:
            if "exceeded the maximum allowed size" in e.args[0]:
                raise MaxAllowedSizeExceeded()


async def get(partition_key: str, sort_key: str) -> str | None:
    async with get_dynamodb_client() as dynamodb:
        response = await dynamodb.get_item(
            TableName=settings.aws_dynamodb_table_name,
            Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        )

    if "Item" not in response:
        return None

    item = response["Item"]["VALUE"]["S"]
    ttl = int(response["Item"]["TTL"]["N"]) if "TTL" in response["Item"] else None

    if ttl:
        return None if _is_expired(ttl) else item

    return item


async def delete(partition_key: str, sort_key: str) -> bool:
    async with get_dynamodb_client() as dynamodb:
        response = await dynamodb.delete_item(
            TableName=settings.aws_dynamodb_table_name,
            Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
            ReturnValues="ALL_OLD",
        )

    # The "delete_item" operation is idempotent.
    # This is a trick to check if an item is deleted or not
    if "Attributes" not in response:
        return False

    attributes = response["Attributes"]
    ttl = int(attributes["TTL"]["N"]) if "TTL" in attributes else None

    return not _is_expired(ttl) if ttl else True


async def get_sort_keys(
    partition_key: str, from_sort_key: str | None = None
) -> tuple[list[str], str | None]:
    async with get_dynamodb_client() as dynamodb:
        query_params = {
            "TableName": settings.aws_dynamodb_table_name,
            "KeyConditionExpression": "PK = :PK",
            "ProjectionExpression": "SK",
            "FilterExpression": "attribute_not_exists(#TTL) or #TTL >= :ttl",
            "ExpressionAttributeNames": {"#TTL": "TTL"},
            "ExpressionAttributeValues": {
                ":PK": {"S": partition_key},
                ":ttl": {"N": str(get_current_timestamp())},
            },
        }

        if from_sort_key is not None:
            query_params["ExclusiveStartKey"] = {
                "PK": {"S": partition_key},
                "SK": {"S": from_sort_key},
            }

        response = await dynamodb.query(**query_params)

    last_evaluated_key = (
        response["LastEvaluatedKey"]["SK"]["S"]
        if "LastEvaluatedKey" in response
        else None
    )

    return [elem["SK"]["S"] for elem in response["Items"]], last_evaluated_key


async def get_sort_values(
    partition_key: str, from_sort_key: str | None = None
) -> tuple[list[str], str | None]:
    async with get_dynamodb_client() as dynamodb:
        query_params = {
            "TableName": settings.aws_dynamodb_table_name,
            "KeyConditionExpression": "PK = :PK",
            "ProjectionExpression": "#VALUE",
            "FilterExpression": "attribute_not_exists(#TTL) or #TTL >= :ttl",
            "ExpressionAttributeNames": {"#TTL": "TTL", "#VALUE": "VALUE"},
            "ExpressionAttributeValues": {
                ":PK": {"S": partition_key},
                ":ttl": {"N": str(get_current_timestamp())},
            },
        }

        if from_sort_key is not None:
            query_params["ExclusiveStartKey"] = {
                "PK": {"S": partition_key},
                "SK": {"S": from_sort_key},
            }

        response = await dynamodb.query(**query_params)

    last_evaluated_key = (
        response["LastEvaluatedKey"]["SK"]["S"]
        if "LastEvaluatedKey" in response
        else None
    )

    return [elem["VALUE"]["S"] for elem in response["Items"]], last_evaluated_key


def _is_expired(ttl: int) -> bool:
    return ttl < get_current_timestamp()


def get_current_timestamp() -> int:
    return int((datetime.utcnow()).timestamp())
