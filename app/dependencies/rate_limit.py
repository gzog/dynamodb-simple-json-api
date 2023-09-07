import time
from fastapi import Request, HTTPException
from app.settings import settings, Environment

# Allowed requests per second
REQUESTS = 10


class Cache:
    def __init__(self):
        self.cache = {}

    def set(self, key, value, ttl):
        expire_time = time.time() + ttl
        self.cache[key] = {"value": value, "expire_time": expire_time}

    def get(self, key):
        cur_time = time.time()
        if key in self.cache:
            if self.cache[key]["expire_time"] > cur_time:
                return self.cache[key]["value"]
            else:
                del self.cache[key]
        return None

    def evict_expired(self):
        cur_time = time.time()
        keys_to_evict = [
            key for key, item in self.cache.items() if item["expire_time"] <= cur_time
        ]
        for key in keys_to_evict:
            del self.cache[key]


cache = Cache()


class RateLimitAPIKey:
    def __call__(self, request: Request) -> None:
        api_key = request.state.api_key

        if settings.environment == Environment.Local:
            return

        number_of_requests = cache.get(api_key) or 0

        if number_of_requests > REQUESTS:
            raise HTTPException(status_code=429, detail="Too many requests")

        cache.set(api_key, number_of_requests + 1, 5)
