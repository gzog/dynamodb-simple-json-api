from fastapi.testclient import TestClient
from app.settings import settings
from pytest import fixture

from app.main import api


@fixture(scope="session")
def client() -> TestClient:
    return TestClient(api, headers={"Authorization": f"Bearer {settings.api_key}"})
