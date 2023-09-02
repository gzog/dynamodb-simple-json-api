from app.settings import settings
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN


class HTTPBearerAPIKey(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        result: HTTPAuthorizationCredentials = await super().__call__(request)

        if result.credentials != settings.api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="API Key is invalid"
            )

        return result
