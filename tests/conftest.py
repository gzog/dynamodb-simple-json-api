from fastapi.testclient import TestClient
from pytest import fixture
from app.main import api


@fixture(scope="session")
def client() -> TestClient:
    return TestClient(api)
