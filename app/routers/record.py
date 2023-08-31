from fastapi import APIRouter, Body, Request, Response, status
from fastapi.responses import JSONResponse

from app.routers.schemas import KeyPath
from app.services import record as record_service

router = APIRouter(prefix="/record")


@router.post(
    "/{key}",
)
async def create_or_update_record(
    request: Request, key: str = KeyPath, payload: dict = Body(...)
) -> Response:
    await record_service.create_or_update_record(request.state.api_key, key, payload)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{key}",
)
async def delete_record(request: Request, key: str = KeyPath) -> Response:
    deleted = await record_service.delete_record(request.state.api_key, key)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND
    )


@router.get(
    "/{key}",
)
async def get_record(request: Request, key: str = KeyPath) -> JSONResponse:
    value = await record_service.get_record_value(request.state.api_key, key)
    return JSONResponse(
        content=value,
        status_code=status.HTTP_200_OK
        if value is not None
        else status.HTTP_404_NOT_FOUND,
    )
