from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.logger import logger


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        logger.info(
            "http",
            extra={
                "req": {"method": request.method, "url": str(request.url)},
                "res": {
                    "code": response.status_code,
                },
            },
        )
        return response
