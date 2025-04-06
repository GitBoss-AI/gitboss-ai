# backend/app/controllers/contributors.py
import logging
from typing import Dict, List, Optional, Any

from app.services.github.contributors import GitHubContributorsService

logger = logging.getLogger(__name__)


class ContributorsController:
    """Controller for contributor-related operations."""

    def __init__(self):
        self.github_service = GitHubContributorsService()

    async def get_repository_contributors(self, owner: str, repo: str, start_date: Optional[str] = None,
                                          end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get repository contributors with their statistics."""

        logger.info(f"Fetching contributors for {owner}/{repo} from {start_date} to {end_date}")

        try:
            contributors = self.github_service.get_repository_contributors(
                owner=owner,
                repo=repo,
                start_date=start_date,
                end_date=end_date
            )

            logger.info(f"Successfully fetched {len(contributors)} contributors for {owner}/{repo}")
            return contributors
        except Exception as e:
            logger.error(f"Error fetching repository contributors: {str(e)}")
            raise e

    async def get_contributor_weekly_stats(self, owner: str, repo: str, weeks: int = 4) -> Dict[str, Any]:
        """Get weekly statistics for each contributor."""

        logger.info(f"Fetching weekly stats for contributors of {owner}/{repo} for {weeks} weeks")

        try:
            weekly_stats = self.github_service.get_contributor_weekly_stats(
                owner=owner,
                repo=repo,
                weeks=weeks
            )

            logger.info(f"Successfully fetched weekly stats for contributors of {owner}/{repo}")
            return weekly_stats
        except Exception as e:
            logger.error(f"Error fetching weekly contributor stats: {str(e)}")
            raise e