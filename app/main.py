from fastapi import FastAPI
from app.routers import item
from app.middlewares.size import LimitUploadSizeMiddleware
from app.middlewares.log import LogMiddleware
from app.settings import settings, Environment
import sentry_sdk

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

print("dasdad")
