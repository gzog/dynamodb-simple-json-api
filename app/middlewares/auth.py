from typing import Callable

from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.settings import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        auth = request.headers.get("Authorization")
        if not auth:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        token = auth.replace("Bearer ", "")
        if token != settings.api_key:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        return await call_next(request)
