from fastapi import APIRouter
from app.api.v1 import chat, search

# Create the main API router
api_router = APIRouter()

# Include chat and search routers without prefixes since they're already under /api/v1
api_router.include_router(chat.router, prefix="", tags=["chat"])
api_router.include_router(search.router, prefix="", tags=["search"])
