import json
from app import dynamodb
from fastapi.encoders import jsonable_encoder


async def create_or_update_item(key: str, payload: dict) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    await dynamodb.put_item(*get_user_item_primary_key(key), value)


async def get_item_value(key: str) -> dict | None:
    value_str = await dynamodb.get_item(*get_user_item_primary_key(key))
    return value_str and json.loads(value_str)


async def delete_item(key: str) -> bool:
    return await dynamodb.delete_item(*get_user_item_primary_key(key))


def get_user_item_primary_key(key: str):
    partition_key = f"USER#1#KEY#{key}"
    sort_key = f"USER#1#KEY#{key}"
    return partition_key, sort_key
