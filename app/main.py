from fastapi import FastAPI
from functools import lru_cache
from app.routers import item
from app.middlewares.log import LogMiddleware
from app.settings import settings
import sentry_sdk


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=0,
)

api = FastAPI()
api.add_middleware(LogMiddleware)
api.include_router(item.router)

# api.include_router(auth.router)
