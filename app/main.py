import sentry_sdk
from fastapi import FastAPI

from app.middlewares.log import LogMiddleware
from app.middlewares.size import LimitUploadSizeMiddleware
from app.routers import item
from app.settings import Environment, settings

if settings.environment == Environment.Production:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.1,
    )

api = FastAPI()

api.add_middleware(LimitUploadSizeMiddleware, max_upload_size=128_000)  # 128KB
api.add_middleware(LogMiddleware)

api.include_router(item.router)

# api.include_router(auth.router)
