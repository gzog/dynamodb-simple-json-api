import httpx
import pytest
from httpx import Response
from fastapi.testclient import TestClient


class TestCreateOrUpdateRecord:
    def test_success(self, client: TestClient):
        response: Response = client.post(
            "/record/key",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.CREATED

    def test_invalid_key(self, client):
        ...

    def test_invalid_payload(self, client):
        ...

    def test_invalid_user(self, client):
        ...


class TestGetRecord:
    def test_success(self, client: TestClient):
        response: Response = client.get("/record/key")

        assert response.status_code == httpx.codes.OK
        assert response.json() == {"value": {"hello": "world"}}

    def test_not_found(self, client):
        response: Response = client.get("/record/not-found-key")

        assert response.status_code == httpx.codes.NOT_FOUND


class TestDeleteRecord:
    @pytest.mark.parametrize(
        ("key", "expected_http_status_code"),
        [
            ("key", httpx.codes.NO_CONTENT),
            ("not-found-key", httpx.codes.NOT_FOUND),
        ],
    )
    def test_endpoint(self, client: TestClient, key: str, expected_http_status_code: int):
        response: Response = client.delete(f"/record/{key}")

        assert response.status_code == expected_http_status_code
