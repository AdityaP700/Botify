from typing import Any, Dict, Optional

class BotifyException(Exception):
    """Base exception for Botify application"""
    def __init__(
        self,
        message: str,
        error_code: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)

class RateLimitExceeded(BotifyException):
    """Raised when rate limit is exceeded"""
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429
        )

class ValidationError(BotifyException):
    """Raised when input validation fails"""
    def __init__(self, message: str, details: Dict[str, Any]):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )

class DatabaseError(BotifyException):
    """Raised when database operations fail"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            status_code=500,
            details=details
        )

class AIServiceError(BotifyException):
    """Raised when AI service operations fail"""
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AI_SERVICE_ERROR",
            status_code=503,
            details=details
        )

class AuthenticationError(BotifyException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )

class AuthorizationError(BotifyException):
    """Raised when authorization fails"""
    def __init__(self, message: str = "Not authorized"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403
        )
