# backend/app/controllers/repositories.py
import logging
from typing import Dict, Optional, Any

from app.services.github.repos import GitHubRepositoryService

logger = logging.getLogger(__name__)


class RepositoryController:
    """Controller for repository-related operations."""

    def __init__(self):
        self.github_service = GitHubRepositoryService()

    async def get_repository_stats(self, owner: str, repo: str, start_date: Optional[str] = None,
                                   end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get repository statistics for a specific time period."""

        logger.info(f"Fetching stats for {owner}/{repo} from {start_date} to {end_date}")

        try:
            stats = self.github_service.get_repository_stats(
                owner=owner,
                repo=repo,
                start_date=start_date,
                end_date=end_date
            )

            logger.info(f"Successfully fetched stats for {owner}/{repo}")
            return stats
        except Exception as e:
            logger.error(f"Error fetching repository stats: {str(e)}")
            raise e