from app.utils.aws import dynamodb
from datetime import datetime
from app.settings import settings


def create_or_update(
    partition_key: str, sort_key: str, value: str, ttl: int | None
) -> None:
    item = {"PK": {"S": partition_key}, "SK": {"S": sort_key}, "VALUE": {"S": value}}

    if ttl:
        item["TTL"] = {"N": str(ttl)}

    dynamodb.put_item(
        TableName=settings.aws_dynamodb_table_name,
        Item=item,
    )


def get(partition_key: str, sort_key: str) -> str | None:
    response = dynamodb.get_item(
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


def delete(partition_key: str, sort_key: str) -> bool:
    response = dynamodb.delete_item(
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


def get_sort_keys(partition_key: str) -> list[str]:
    response = dynamodb.query(
        TableName=settings.aws_dynamodb_table_name,
        KeyConditionExpression="PK = :PK",
        ProjectionExpression="SK",
        FilterExpression="attribute_not_exists(#TTL) or #TTL >= :ttl",
        ExpressionAttributeNames={"#TTL": "TTL"},
        ExpressionAttributeValues={
            ":PK": {"S": partition_key},
            ":ttl": {"N": str(get_current_timestamp())},
        },
    )

    return [elem["SK"]["S"] for elem in response["Items"]]


def _is_expired(ttl: int):
    return ttl < get_current_timestamp()


def get_current_timestamp():
    return int((datetime.utcnow()).timestamp())
