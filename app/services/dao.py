from app.utils.aws import dynamodb


def create_or_update(
    partition_key: str, sort_key: str, value: str, ttl: int | None
) -> None:
    item = {"PK": {"S": partition_key}, "SK": {"S": sort_key}, "VALUE": {"S": value}}

    if ttl:
        item["TTL"] = {"N": str(ttl)}

    dynamodb.put_item(
        TableName="data",
        Item=item,
    )


def get(partition_key: str, sort_key: str) -> str | None:
    response = dynamodb.get_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
    )

    if "Item" not in response:
        return None

    item = response["Item"]["VALUE"]["S"]
    ttl = response["Item"].get("TTL")

    if ttl:
        pass

    return item


def delete(partition_key: str, sort_key: str) -> bool:
    response = dynamodb.delete_item(
        TableName="data",
        Key={"PK": {"S": partition_key}, "SK": {"S": sort_key}},
        ReturnValues="ALL_OLD",
    )

    # The "delete_item" operation is idempotent.
    # This is a trick to check if an item is deleted or not
    if "Attributes" not in response:
        return False

    attributes = response["Attributes"]

    ttl = attributes.get("TTL")

    if ttl:
        pass

    return True
