# backend/app/routers/repositories.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
import logging

from app.controllers.repos import RepositoryController

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/repos", tags=["repositories"])


@router.get("/{owner}/{repo}/stats")
async def get_repository_stats(
        owner: str,
        repo: str,
        start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
        end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
        controller: RepositoryController = Depends(RepositoryController)
):
    """Get repository statistics for a specific time period."""

    try:
        return await controller.get_repository_stats(
            owner=owner,
            repo=repo,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch repository stats: {str(e)}"
        )