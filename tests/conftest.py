from fastapi.testclient import TestClient
from app.settings import settings
from pytest import fixture

from app.main import api
from app.services.api_key import create_or_update_user


@fixture(scope="session")
def user() -> dict:
    create_or_update_user(settings.api_key, {"id": 5, "name": "George"})


@fixture(scope="session")
def client(user: dict) -> TestClient:
    return TestClient(api, headers={"Authorization": f"Bearer {settings.api_key}"})
