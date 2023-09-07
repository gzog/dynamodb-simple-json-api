import pytest
import asyncio
from fastapi.testclient import TestClient
from app.settings import settings
from pytest import fixture

from app.main import api
from app.services.api_key import create_or_update_user


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> asyncio.unix_events._UnixSelectorEventLoop:
    """Overrides pytest default function scoped event loop"""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@fixture(scope="session", autouse=True)
def user(event_loop: asyncio.unix_events._UnixSelectorEventLoop) -> dict:
    event_loop.run_until_complete(
        create_or_update_user(settings.api_key, {"id": 5, "name": "George"})
    )


@fixture(scope="session", autouse=True)
def client() -> TestClient:
    return TestClient(app=api, headers={"Authorization": f"Bearer {settings.api_key}"})
