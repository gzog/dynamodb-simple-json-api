import json

from fastapi.encoders import jsonable_encoder

from app.services import dao


async def create_or_update_record(
    user_id: str, key: str, payload: dict, ttl: int | None
) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    await dao.create_or_update(*get_primary_key(user_id, key), value, ttl)


async def get_record_value(user_id: str, key: str) -> dict | None:
    value_str = await dao.get(*get_primary_key(user_id, key))
    return json.loads(value_str) if value_str else None


async def delete_record(user_id: str, key: str) -> bool:
    return await dao.delete(*get_primary_key(user_id, key))


async def get_record_keys(user_id: str) -> list[str]:
    return await dao.get_sort_keys(get_partition_key(user_id))


async def get_records(user_id: str) -> list[dict]:
    value_strs = await dao.get_sort_values(get_partition_key(user_id))
    return [json.loads(value_str) for value_str in value_strs]


def get_primary_key(user_id: str, key: str) -> tuple[str, str]:
    return get_partition_key(user_id), get_sort_key(key)


def get_partition_key(user_id: str) -> str:
    return f"USER#{user_id}"


def get_sort_key(key: str) -> str:
    return f"RECORD_KEY#{key}"
