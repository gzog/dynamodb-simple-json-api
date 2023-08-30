from collections import defaultdict
from time import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit: int = 5, time_interval: int = 60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_interval = time_interval
        self.clients: defaultdict[str, list[float]] = defaultdict(list[float])

    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host
        current_time = time()

        if client_ip in self.clients:
            self.clients[client_ip] = [
                t
                for t in self.clients[client_ip]
                if current_time - t < self.time_interval
            ]

        if len(self.clients[client_ip]) >= self.rate_limit:
            return Response(status_code=429)
        else:
            self.clients[client_ip].append(current_time)

        response = await call_next(request)
        return response