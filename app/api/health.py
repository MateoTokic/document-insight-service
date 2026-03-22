from fastapi import APIRouter
from app.services.cache_state import cache_service

router = APIRouter()

@router.get("/health")
def health_check():
    redis_ok = cache_service.ping()
    return {
        "status": "ok",
        "redis": "connected" if redis_ok else "not connected"
    }