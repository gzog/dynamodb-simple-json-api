import json

from fastapi.encoders import jsonable_encoder

from app.services import dao


async def create_or_update_record(
    api_key: str, key: str, payload: dict, ttl: int | None
) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    dao.create_or_update(*get_primary_key(api_key, key), value, ttl)


async def get_record_value(api_key: str, key: str) -> dict | None:
    value_str = dao.get(*get_primary_key(api_key, key))
    return json.loads(value_str) if value_str else None


async def delete_record(api_key: str, key: str) -> bool:
    return dao.delete(*get_primary_key(api_key, key))


async def get_record_keys(api_key: str) -> list[str]:
    return dao.get_sort_keys(get_partition_key(api_key))


def get_primary_key(api_key: str, key: str) -> tuple[str, str]:
    return get_partition_key(api_key), get_sort_key(key)


def get_partition_key(api_key: str) -> str:
    return f"API_KEY{api_key}"


def get_sort_key(key: str) -> str:
    return f"KEY#{key}"
