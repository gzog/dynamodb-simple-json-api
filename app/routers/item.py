from fastapi import APIRouter, Body, Response, status
from fastapi.responses import JSONResponse
from app.services import item as item_service
from app.schemas import KeyPath

router = APIRouter(prefix="/item")


@router.post(
    "/{key}",
)
async def create_or_update_item(
    key: str = KeyPath, payload: dict = Body(...)
) -> Response:
    await item_service.create_or_update_item(key, payload)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/{key}",
)
async def delete_item(key: str = KeyPath) -> Response:
    deleted = await item_service.delete_item(key)
    return Response(
        status_code=status.HTTP_204_NO_CONTENT if deleted else status.HTTP_404_NOT_FOUND
    )


@router.get(
    "/{key}",
)
async def get_item(key: str = KeyPath) -> JSONResponse:
    value = await item_service.get_item_value(key)
    return JSONResponse(
        content=value,
        status_code=status.HTTP_200_OK if value else status.HTTP_404_NOT_FOUND,
    )
