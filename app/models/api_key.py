from app.utils.aws import dynamodb


async def put_api_key(item_key: str, value: str) -> None:
    partition_key, sort_key = get_item_primary_key(item_key)
    dynamodb.put_item(
        TableName="data",
        Item={
            "PK": {"S": partition_key},
            "SK": {"S": sort_key},
            "VALUE": {"S": value},
        },
    )


async def get_api_key(item_key: str) -> str | None:
    partition_key, sort_key = get_item_primary_key(item_key)
    response = dynamodb.get_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
    )
    return response["Item"]["VALUE"]["S"] if "Item" in response else None


async def delete_api_key(item_key: str) -> bool:
    partition_key, sort_key = get_item_primary_key(item_key)
    response = dynamodb.delete_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        ReturnValues="ALL_OLD",
    )

    # The "delete_item" operation is idempotent.
    # This is a trick to check if an item is deleted or not
    return "Attributes" in response


def get_item_primary_key(key: str) -> tuple[str, str]:
    partition_key = f"API_KEY#{key}"
    sort_key = "USER#USER_1"
    return partition_key, sort_key
