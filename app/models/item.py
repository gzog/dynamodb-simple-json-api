from app.utils.aws import dynamodb


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
    response = dynamodb.get_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
    )
    return response["Item"]["VALUE"]["S"] if "Item" in response else None


async def delete_item(partition_key: str, sort_key) -> bool:
    response = dynamodb.delete_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        ReturnValues="ALL_OLD",
    )

    # The "delete_item" operation is idempotent.
    # This is a trick to check if an item is deleted or not
    return "Attributes" in response
