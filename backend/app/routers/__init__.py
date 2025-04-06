from fastapi import APIRouter

from app.routers.health import router as health_router
from app.routers.repos import router as repository_router
from app.routers.contributors import router as contributors_router
from app.routers.websockets import router as websocket_router

# Create main router
router = APIRouter()

# Include all routers
router.include_router(health_router)
router.include_router(repository_router)
router.include_router(contributors_router)
router.include_router(websocket_router)