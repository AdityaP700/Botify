from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import time
import asyncio
from typing import Dict, Optional
from datetime import datetime, timedelta
from app.core.config import settings
from app.core.exceptions import RateLimitExceeded
from app.core.logger import logger

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.rate_limit = settings.RATE_LIMIT_PER_MINUTE
        self.window = 60  # 1 minute window
        self.requests: Dict[str, list] = {}
        self._cleanup_task = asyncio.create_task(self._cleanup_old_requests())

    async def _cleanup_old_requests(self):
        while True:
            current_time = datetime.now()
            for ip in list(self.requests.keys()):
                self.requests[ip] = [
                    timestamp for timestamp in self.requests[ip]
                    if current_time - timestamp < timedelta(seconds=self.window)
                ]
                if not self.requests[ip]:
                    del self.requests[ip]
            await asyncio.sleep(10)  # Cleanup every 10 seconds

    def _get_ip(self, request: Request) -> str:
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0]
        return request.client.host if request.client else "unknown"

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health check
        if request.url.path == "/health":
            return await call_next(request)

        ip = self._get_ip(request)
        now = datetime.now()

        # Initialize request list for IP if not exists
        if ip not in self.requests:
            self.requests[ip] = []

        # Remove old requests outside the window
        self.requests[ip] = [
            timestamp for timestamp in self.requests[ip]
            if now - timestamp < timedelta(seconds=self.window)
        ]

        # Check rate limit
        if len(self.requests[ip]) >= self.rate_limit:
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            raise RateLimitExceeded()

        # Add current request
        self.requests[ip].append(now)

        # Process request and measure timing
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add custom headers
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Rate-Limit-Limit"] = str(self.rate_limit)
        response.headers["X-Rate-Limit-Remaining"] = str(
            self.rate_limit - len(self.requests[ip])
        )
        response.headers["X-Rate-Limit-Reset"] = str(
            int(self.window - (time.time() % self.window))
        )

        return response

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Response: {response.status_code} "
                f"Process Time: {process_time:.3f}s "
                f"Path: {request.url.path}"
            )
            
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error: {str(e)} "
                f"Process Time: {process_time:.3f}s "
                f"Path: {request.url.path}",
                exc_info=True
            )
            raise
