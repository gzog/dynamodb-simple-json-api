from fastapi import FastAPI
from app.routers import item
from app.middlewares.log import LogMiddleware
from app.settings import settings
import sentry_sdk


if settings.environment == "production":
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        traces_sample_rate=0.1,
    )

api = FastAPI()
api.add_middleware(LogMiddleware)
api.include_router(item.router)

# api.include_router(auth.router)
