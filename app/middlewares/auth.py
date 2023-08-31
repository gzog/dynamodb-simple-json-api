from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.settings import settings


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        auth = request.headers.get("Authorization")
        if not auth:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)

        api_key = auth.replace("Bearer ", "")

        # TODO: Support additional api keys
        if api_key != settings.api_key:
            return Response(status_code=status.HTTP_403_FORBIDDEN)

        request.state.api_key = api_key

        return await call_next(request)
