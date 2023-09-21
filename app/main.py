import sentry_sdk
from fastapi import FastAPI, Request, Response
from starlette import status

from app.exceptions import RateLimitExceeded, MaxAllowedSizeExceeded
from app.middlewares.log import LogMiddleware
from app.middlewares.size import LimitUploadSizeMiddleware
from app.routers.record import records_router
from app.settings import Environment, settings
from fastapi import Security, Depends
from app.dependencies.rate_limit import RateLimitAPIKey
from app.dependencies.auth import HTTPBearerAPIKey

if settings.environment == Environment.Production:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.1,
    )

bearer = HTTPBearerAPIKey()


api = FastAPI(
    title="DynamoDB Simple JSON API",
    dependencies=[Security(bearer), Depends(RateLimitAPIKey())],
)

api.add_middleware(LimitUploadSizeMiddleware)  # 400KB
api.add_middleware(LogMiddleware)

api.include_router(records_router)


@api.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(
    request: Request, exc: RateLimitExceeded
) -> Response:
    return Response(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )


@api.exception_handler(MaxAllowedSizeExceeded)
async def max_allowed_size_exceeded_exception_handler(
    request: Request, exc: RateLimitExceeded
) -> Response:
    return Response(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    )
