from fastapi import FastAPI
from app.routers import item, auth
import sentry_sdk


sentry_sdk.init(
    dsn="https://b5c2f49ccf20cdd5daec6f03d656cbdc@o4504411712258048.ingest.sentry.io/4505773483950080",
    traces_sample_rate=0,
)


api = FastAPI()
api.include_router(item.router)
# api.include_router(auth.router)
