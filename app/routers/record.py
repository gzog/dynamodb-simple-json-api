from fastapi import APIRouter, Body, Response, status
from fastapi.responses import JSONResponse
from fastapi import Security
from fastapi.security.http import HTTPAuthorizationCredentials
from app.routers.schemas import KeyPath
from app.dependencies.auth import HTTPBearerAPIKey
from app.services import record as record_service

router = APIRouter(prefix="/record")

bearer = HTTPBearerAPIKey()


@router.get(
    "/keys",
)
async def get_record_keys(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
) -> JSONResponse:
    keys = await record_service.get_record_keys(credentials.credentials)
    return JSONResponse(
        content=keys,
        status_code=status.HTTP_200_OK,
    )


@router.post(
    "/{key}",
)
async def create_or_update_record(
    credentials: HTTPAuthorizationCredentials = Security(bearer),
    key: str = KeyPath,
    payload: dict = Body(...),
    ttl: int | None = None,
) -> Response:
    await record_service.create_or_update_record(
        credentials.credentials, key, payload, ttl
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{key}",
)
async def delete_record(
    credentials: HTTPAuthorizationCredentials = Security(bearer), key: str = KeyPath
) -> Response:
    deleted = await record_service.delete_record(credentials.credentials, key)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND
    )


@router.get(
    "/{key}",
)
async def get_record(
    credentials: HTTPAuthorizationCredentials = Security(bearer), key: str = KeyPath
) -> JSONResponse:
    value = await record_service.get_record_value(credentials.credentials, key)
    return JSONResponse(
        content=value,
        status_code=status.HTTP_200_OK
        if value is not None
        else status.HTTP_404_NOT_FOUND,
    )
