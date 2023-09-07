from app.services.api_key import get_user
from app.utils.cache import cache
from fastapi import Request, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class HTTPAuthorizationCredentialsWithUser(HTTPAuthorizationCredentials):
    user: dict


class HTTPBearerAPIKey(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> HTTPAuthorizationCredentialsWithUser | None:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)

        if not credentials:
            return None

        api_key = credentials.credentials

        user = cache.get(api_key)
        if not user:
            user = await get_user(api_key)

        if not user:
            raise HTTPException(status_code=401, detail="Invalid API Key")

        cache.set(api_key, user, 1)

        result = HTTPAuthorizationCredentialsWithUser(
            scheme=credentials.scheme, credentials=credentials.credentials, user=user
        )

        request.state.api_key = api_key
        request.state.user = user
        return result
