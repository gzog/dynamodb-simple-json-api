from fastapi import Request, HTTPException
from app.settings import settings, Environment
from app.utils.cache import cache

# Allowed requests per second
REQUESTS = 10


class RateLimitAPIKey:
    def __call__(self, request: Request) -> None:
        api_key = request.state.api_key

        if settings.environment != Environment.Production:
            return

        number_of_requests = cache.get(api_key) or 0

        if number_of_requests > REQUESTS:
            raise HTTPException(status_code=429, detail="Too many requests")

        cache.set(api_key, number_of_requests + 1, 5)
