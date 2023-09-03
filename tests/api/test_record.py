from datetime import datetime
from dateutil.relativedelta import relativedelta
import httpx
import pytest
from httpx import Response
from fastapi.testclient import TestClient


class TestCreateOrUpdateRecord:
    def test_create_without_ttl(self, client: TestClient):
        response: Response = client.post(
            "/record/key",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.CREATED

    def test_create_with_valid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() + relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/record/key_ttl?ttl={ttl}",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.CREATED

    def test_create_with_invalid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() - relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/record/key_ttl?ttl={ttl}",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.CREATED

    def test_invalid_key(self, client: TestClient):
        response: Response = client.post(
            "/record/@.!@#$%'",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
        assert response.json() == {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["path", "key"],
                    "msg": "String should match pattern '[a-z0-9-]+'",
                    "input": "@.!@",
                    "ctx": {"pattern": "[a-z0-9-]+"},
                    "url": "https://errors.pydantic.dev/2.3/v/string_pattern_mismatch",
                }
            ]
        }

    def test_invalid_payload(self, client: TestClient):
        response: Response = client.post(
            "/record/invalid_payload",
            content="bla",
        )

        assert response.status_code == httpx.codes.UNPROCESSABLE_ENTITY
        assert response.json() == {
            "detail": [
                {
                    "type": "json_invalid",
                    "loc": ["body", 0],
                    "msg": "JSON decode error",
                    "input": {},
                    "ctx": {"error": "Expecting value"},
                }
            ]
        }


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
