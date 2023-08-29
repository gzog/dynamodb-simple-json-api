import json

from fastapi.encoders import jsonable_encoder

from app.models import item


async def create_or_update_item(key: str, payload: dict) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    await item.put_item(*get_user_item_primary_key(key), value)


async def get_item_value(key: str) -> dict | None:
    value_str = await item.get_item(*get_user_item_primary_key(key))
    return json.loads(value_str) if value_str else None


async def delete_item(key: str) -> bool:
    return await item.delete_item(*get_user_item_primary_key(key))


def get_user_item_primary_key(key: str) -> tuple[str, str]:
    partition_key = f"USER#1#KEY#{key}"
    sort_key = f"USER#1#KEY#{key}"
    return partition_key, sort_key
