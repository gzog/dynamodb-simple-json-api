import json

from fastapi.encoders import jsonable_encoder

from app.models import item


async def create_or_update_item(item_key: str, payload: dict) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    await item.put_item(item_key, value)


async def get_item_value(item_key: str) -> dict | None:
    value_str = await item.get_item(item_key)
    return json.loads(value_str) if value_str else None


async def delete_item(item_key: str) -> bool:
    return await item.delete_item(item_key)
