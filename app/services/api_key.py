import json
from app.services import dao
from fastapi.encoders import jsonable_encoder


def get_partition_key(api_key: str) -> str:
    return f"API_KEY#{api_key}"


def get_sort_key(api_key: str) -> str:
    return f"API_KEY#{api_key}"


def get_primary_key(api_key: str) -> tuple[str, str]:
    return get_partition_key(api_key), get_sort_key(api_key)


def get_user(api_key: str):
    value_str = dao.get(*get_primary_key(api_key))
    return json.loads(value_str) if value_str else None


def create_or_update_user(api_key: str, payload: dict, ttl: int | None = None) -> None:
    jsonable_payload = jsonable_encoder(payload)
    value = json.dumps(jsonable_payload)
    dao.create_or_update(*get_primary_key(api_key), value, ttl)
