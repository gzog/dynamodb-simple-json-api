from fastapi import APIRouter, Body, Response, Request, status
from fastapi.responses import JSONResponse
from app.routers.schemas import KeyPath
from app.services import record as record_service

records_router = APIRouter(prefix="/records")


@records_router.get(
    "/keys",
)
async def get_record_keys(
    request: Request,
) -> JSONResponse:
    keys = await record_service.get_record_keys(request.state.user["id"])
    return JSONResponse(
        content=keys,
        status_code=status.HTTP_200_OK,
    )


@records_router.get(
    "",
)
async def get_records(
    request: Request,
) -> JSONResponse:
    records = await record_service.get_records(request.state.user["id"])
    return JSONResponse(
        content=records,
        status_code=status.HTTP_200_OK,
    )


@records_router.post(
    "/{key}",
)
async def create_or_update_record(
    request: Request,
    key: str = KeyPath,
    payload: dict = Body(...),
    ttl: int | None = None,
) -> Response:
    await record_service.create_or_update_record(
        request.state.user["id"], key, payload, ttl
    )
    return Response(status_code=status.HTTP_201_CREATED)


@records_router.delete(
    "/{key}",
)
async def delete_record(
    request: Request,
    key: str = KeyPath,
) -> Response:
    deleted = await record_service.delete_record(request.state.user["id"], key)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND
    )


@records_router.get(
    "/{key}",
)
async def get_record(
    request: Request,
    key: str = KeyPath,
) -> JSONResponse:
    value = await record_service.get_record_value(request.state.user["id"], key)
    return JSONResponse(
        content=value,
        status_code=status.HTTP_200_OK
        if value is not None
        else status.HTTP_404_NOT_FOUND,
    )
