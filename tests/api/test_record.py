from datetime import datetime
from dateutil.relativedelta import relativedelta
from fastapi import status
from httpx import Response
from fastapi.testclient import TestClient


class TestCreateOrUpdateRecord:
    def test_create_record_without_ttl(self, client: TestClient):
        response: Response = client.post(
            "/record/key",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_valid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() + relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/record/key-valid-ttl?ttl={ttl}",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_invalid_ttl(self, client: TestClient):
        ttl = int((datetime.utcnow() - relativedelta(seconds=60)).timestamp())

        response: Response = client.post(
            f"/record/key-expired-ttl?ttl={ttl}",
            json={"hello": "world"},
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_with_invalid_key(self, client: TestClient):
        response: Response = client.post(
            "/record/key-record-@.!@#$%'",
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
            "/record/key-invalid-payload",
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


class TestGetRecord:
    def test_get_record_without_ttl(self, client: TestClient):
        response: Response = client.get("/record/key")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"hello": "world"}

    def test_get_record_with_non_expired_ttl(self, client: TestClient):
        response: Response = client.get("/record/key-valid-ttl")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"hello": "world"}

    def test_get_record_with_expired_ttl(self, client: TestClient):
        response: Response = client.get("/record/key-expired-ttl")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_record_does_not_exist(self, client):
        response: Response = client.get("/record/key-not-found")

        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestGetRecordKeys:
    def test_get_record_keys(self, client: TestClient):
        response: Response = client.get("/records/keys")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == ["KEY#key", "KEY#key-valid-ttl"]


class TestGetRecords:
    def test_get_records(self, client: TestClient):
        response: Response = client.get("/records")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [{"hello": "world"}, {"hello": "world"}]


class TestDeleteRecord:
    def test_delete_existing_record(self, client: TestClient):
        response: Response = client.delete("/record/key")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_existing_record_with_valid_ttl(self, client: TestClient):
        response: Response = client.delete("/record/key-valid-ttl")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_delete_existing_record_with_expired_ttl(self, client: TestClient):
        response: Response = client.delete("/record/key-expired-ttl")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_HTTP_404_NOT_FOUND_record(self, client: TestClient):
        response: Response = client.delete("/record/key-not-found")
        assert response.status_code == status.HTTP_404_NOT_FOUND
