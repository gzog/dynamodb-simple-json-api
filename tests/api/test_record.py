import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import status, Response
from app.services import record as record_service
from app.settings import settings


class TestCreateOrUpdateRecord:
    def test_create_record_without_ttl(self, client: TestClient):
        response: Response = client.post(
            "/records/key",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_valid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() + relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/records/key-valid-ttl?ttl={ttl}",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_invalid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() - relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/records/key-expired-ttl?ttl={ttl}",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_invalid_key(self, client: TestClient):
        response: Response = client.post(
            "/records/key-record-@.!@#$%'",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert response.json() == {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["path", "key"],
                    "msg": "String should match pattern '^[a-z0-9-]+$'",
                    "input": "key-record-@.!@",
                    "ctx": {"pattern": "^[a-z0-9-]+$"},
                    "url": "https://errors.pydantic.dev/2.3/v/string_pattern_mismatch",
                }
            ]
        }

    def test_create_record_with_invalid_payload(self, client: TestClient):
        response: Response = client.post(
            "/records/key-invalid-payload",
            content="bla",
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
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

    def test_create_payload_with_max_size(self, client: TestClient):
        response: Response = client.post(
            "/records/key-big-payload",
            content="t" * (settings.max_upload_size + 1),
        )

        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_create_big_json_payload(self, client: TestClient):
        response: Response = client.post(
            "/records/key-big-payload",
            json={"hello": "world" * settings.max_upload_size},
        )

        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE

    def test_create_almost_big_json_payload(self, client: TestClient):
        response: Response = client.post(
            "/records/key-big-payload",
            json={"h": "w" * (settings.max_upload_size - 9)},
        )

        assert response.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class TestGetRecord:
    def test_get_record_without_ttl(self, client: TestClient):
        response: Response = client.get("/records/key")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"hello": "world"}

    def test_get_record_with_non_expired_ttl(self, client: TestClient):
        response: Response = client.get("/records/key-valid-ttl")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"hello": "world"}

    def test_get_record_with_expired_ttl(self, client: TestClient):
        response: Response = client.get("/records/key-expired-ttl")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_record_does_not_exist(self, client):
        response: Response = client.get("/records/key-not-found")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetRecordKeys:
    def test_get_record_keys(self, client: TestClient):
        response: Response = client.get("/records/keys")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == ["RECORD_KEY#key", "RECORD_KEY#key-valid-ttl"]


class TestGetRecords:
    def test_get_records(self, client: TestClient):
        response: Response = client.get("/records")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{"hello": "world"}, {"hello": "world"}]


class TestDeleteRecord:
    def test_delete_existing_record(self, client: TestClient):
        response: Response = client.delete("/records/key")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_existing_record_with_valid_ttl(self, client: TestClient):
        response: Response = client.delete("/records/key-valid-ttl")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_existing_record_with_expired_ttl(self, client: TestClient):
        response: Response = client.delete("/records/key-expired-ttl")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_HTTP_404_NOT_FOUND_record(self, client: TestClient):
        response: Response = client.delete("/records/key-not-found")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetRecordKeysWithLastEvaluatedKey:
    @pytest.mark.asyncio
    async def test_get_record_keys(self, client: TestClient, user: dict[str, str]):
        for i in range(12):
            await record_service.create_or_update_record(
                user["id"], f"key{i}", {"hello" * 10000: "world" * 10000}, None
            )

        response: Response = client.get("/records/keys")

        assert response.status_code == status.HTTP_200_OK

        assert "x-lastevaluated-key" in response.headers
        assert len(response.json()) == 11


class TestGetRecordKeysWithPaginatedResult:
    @pytest.mark.asyncio
    async def test_get_record_keys_subset(self, client: TestClient, user: dict[str, str]):
        for i in range(12):
            await record_service.create_or_update_record(
                user["id"], f"key{i}", {"hello" * 10000: "world" * 10000}, None
            )

        response: Response = client.get("/records/keys")

        assert response.status_code == status.HTTP_200_OK

        last_evaluated_key = response.headers["x-lastevaluated-key"]
        assert len(response.json()) == 11

        response: Response = client.get(
            "/records/keys", headers={"from-record-key": last_evaluated_key}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1


class TestGetRecordsWithPaginatedResult:
    @pytest.mark.asyncio
    async def test_get_records_subset(self, client: TestClient, user: dict[str, str]):
        response: Response = client.get("/records/")

        assert response.status_code == status.HTTP_200_OK

        last_evaluated_key = response.headers["x-lastevaluated-key"]
        assert len(response.json()) == 11

        response: Response = client.get(
            "/records/", headers={"from-record-key": last_evaluated_key}
        )

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
