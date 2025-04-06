import logging
from typing import Dict, List, Optional, Any

from app.services.github.base import GitHubBaseService

logger = logging.getLogger(__name__)


class GitHubContributorsService(GitHubBaseService):
    """Service for fetching GitHub repository contributor data."""

    def get_repository_contributors(self, owner: str, repo: str, start_date: Optional[str] = None,
                                    end_date: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get repository contributors with statistics."""

        # Get basic list of contributors
        contributors_endpoint = f"repos/{owner}/{repo}/contributors"
        contributors = self.get_paginated_results(contributors_endpoint)

        # Create date filter strings for GitHub search
        date_filter = ""
        if start_date:
            date_filter += f"+committer-date:>={start_date}"
        if end_date:
            date_filter += f"+committer-date:<={end_date}"

        # Detailed contributor stats
        contributor_stats = []

        for contributor in contributors:
            username = contributor.get("login")
            avatar_url = contributor.get("avatar_url")

            # Get commits by this contributor
            commits_query = f"search/commits?q=repo:{owner}/{repo}+author:{username}{date_filter}"
            try:
                commits_data = self.make_request(commits_query)
                commit_count = commits_data.get("total_count", 0)
            except Exception as e:
                logger.error(f"Error fetching commits for {username}: {str(e)}")
                commit_count = 0

            # Get PRs created by this contributor
            prs_query = f"search/issues?q=repo:{owner}/{repo}+author:{username}+is:pr{date_filter.replace('committer-date', 'created')}"
            try:
                prs_data = self.get_paginated_results(prs_query)
                pr_count = len(prs_data)
            except Exception as e:
                logger.error(f"Error fetching PRs for {username}: {str(e)}")
                pr_count = 0

            # Get reviews done by this contributor
            reviews_count = 0
            # Note: GitHub API doesn't provide a direct way to search for reviews by a user
            # We would need to loop through PRs and check if this user reviewed them
            # This is a placeholder for the actual implementation

            # Get recent activity
            recent_activity = self._get_contributor_recent_activity(owner, repo, username)

            contributor_stats.append({
                "username": username,
                "avatar_url": avatar_url,
                "commits": commit_count,
                "pull_requests": pr_count,
                "reviews": reviews_count,
                "total_contributions": commit_count + pr_count + reviews_count,
                "recent_activity": recent_activity
            })

        # Sort by total contributions
        contributor_stats.sort(key=lambda x: x["total_contributions"], reverse=True)

        return contributor_stats

    def _get_contributor_recent_activity(self, owner: str, repo: str, username: str) -> List[Dict[str, Any]]:
        """Get recent activity for a contributor."""
        # TODO
        return None


    def get_contributor_weekly_stats(self, owner: str, repo: str, weeks: int = 4) -> Dict[str, Any]:
        """Get weekly statistics for each contributor."""
        # TODO
        return None