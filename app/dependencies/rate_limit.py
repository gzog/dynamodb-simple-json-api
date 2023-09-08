from fastapi import Request, HTTPException
from app.settings import settings, Environment
from app.utils.cache import cache


class RateLimitAPIKey:
    def __call__(self, request: Request) -> None:
        api_key = request.state.api_key

        if settings.environment != Environment.Production:
            return

        number_of_requests = cache.get(api_key) or 0

        if number_of_requests > settings.requests_per_second:
            raise HTTPException(status_code=429, detail="Too many requests")

        cache.set(api_key, number_of_requests + 1, 5)
