import sentry_sdk
from fastapi import FastAPI, Request, Response
from starlette import status

from app.exceptions import RateLimitExceeded
from app.middlewares.log import LogMiddleware
from app.middlewares.rate_limit import RateLimitMiddleware
from app.middlewares.size import LimitUploadSizeMiddleware
from app.routers.record import record_router, records_router
from app.settings import Environment, settings
from fastapi import Security
from app.dependencies.auth import HTTPBearerAPIKey

if settings.environment == Environment.Production:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.1,
    )

bearer = HTTPBearerAPIKey()

api = FastAPI(dependencies=[Security(bearer)])

api.add_middleware(
    RateLimitMiddleware, rate_limit=60, time_interval=1
)  # 60 requests / sec
api.add_middleware(LimitUploadSizeMiddleware, max_upload_size=400_000)  # 400KB
api.add_middleware(LogMiddleware)

api.include_router(records_router)
api.include_router(record_router)


@api.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
    return Response(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
    )
