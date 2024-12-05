from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a limiter instance
limiter = Limiter(key_func=get_remote_address)

# Rate limit decorator function
def rate_limit(calls_per_minute: int = 30):
    """
    Rate limit decorator that can be applied to API endpoints
    Default: 30 calls per minute
    """
    return limiter.limit(f"{calls_per_minute}/minute")
