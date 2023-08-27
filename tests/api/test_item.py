import pytest
import httpx
from httpx import Response


class TestCreateOrUpdateItem:
    def test_success(self, client):
        response: Response = client.post(
            "/item/key",
            json={"value": {"hello": "world"}},
        )

        assert response.status_code == httpx.codes.CREATED

    def test_invalid_key(self, client):
        ...

    def test_invalid_payload(self, client):
        ...

    def test_invalid_user(self, client):
        ...


class TestGetItem:
    def test_success(self, client):
        response: Response = client.get("/item/key")

        assert response.status_code == httpx.codes.OK
        assert response.json() == {"value": {"hello": "world"}}

    def test_not_found(self, client):
        response: Response = client.get("/item/not-found-key")

        assert response.status_code == httpx.codes.NOT_FOUND


class TestDeleteItem:
    @pytest.mark.parametrize(
        ("key", "expected_http_status_code"),
        [
            ("key", httpx.codes.NO_CONTENT),
            ("not-found-key", httpx.codes.NOT_FOUND),
        ],
    )
    def test_endpoint(self, client, key, expected_http_status_code):
        print(key)
        response: Response = client.delete(f"/item/{key}")

        assert response.status_code == expected_http_status_code
