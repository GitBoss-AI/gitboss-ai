# backend/app/routers/health.py
from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["system"])

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"}