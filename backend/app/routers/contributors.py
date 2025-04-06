# backend/app/routers/contributors.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
import logging

from app.controllers.contributors import ContributorsController

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/contributors", tags=["contributors"])


@router.get("/{owner}/{repo}")
async def get_repository_contributors(
        owner: str,
        repo: str,
        start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
        end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format"),
        controller: ContributorsController = Depends(ContributorsController)
):
    """Get repository contributors with their statistics."""

    try:
        return await controller.get_repository_contributors(
            owner=owner,
            repo=repo,
            start_date=start_date,
            end_date=end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch repository contributors: {str(e)}"
        )


@router.get("/{owner}/{repo}/weekly")
async def get_contributor_weekly_stats(
        owner: str,
        repo: str,
        weeks: int = Query(4, description="Number of weeks to include in the statistics"),
        controller: ContributorsController = Depends(ContributorsController)
):
    """Get weekly statistics for each contributor."""

    try:
        return await controller.get_contributor_weekly_stats(
            owner=owner,
            repo=repo,
            weeks=weeks
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weekly contributor stats: {str(e)}"
        )