import json

from fastapi.encoders import jsonable_encoder

from app.services import dao


async def create_or_update_record(api_key: str, key: str, payload: dict) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    dao.create_or_update(*get_primary_key(api_key, key), value)


async def get_record_value(api_key: str, key: str) -> dict | None:
    value_str = dao.get(*get_primary_key(api_key, key))
    return json.loads(value_str) if value_str else None


async def delete_record(api_key: str, key: str) -> bool:
    return dao.delete(*get_primary_key(api_key, key))


def get_primary_key(api_key: str, key: str) -> tuple[str, str]:
    partition_key = f"API_KEY{api_key}#KEY#{key}"
    sort_key = f"API_KEY{api_key}#KEY#{key}"
    return partition_key, sort_key
