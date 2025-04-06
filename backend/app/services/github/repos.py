import logging
import re
from typing import Dict, Optional, Any

from app.services.github.base import GitHubBaseService

logger = logging.getLogger(__name__)


class GitHubRepositoryService(GitHubBaseService):
    """Service for interacting with GitHub repository data."""

    def get_repository_stats(self, owner: str, repo: str, start_date: Optional[str] = None,
                             end_date: Optional[str] = None) -> Dict[str, Any]:
        """Get repository statistics for a specific time period."""

        # Get basic repository info
        repo_info = self.make_request(f"repos/{owner}/{repo}")

        # Get commits with date filter if provided
        commits_query = f"repos/{owner}/{repo}/commits"
        commits_params = {}

        if start_date:
            commits_params["since"] = f"{start_date}T00:00:00Z"
        if end_date:
            commits_params["until"] = f"{end_date}T23:59:59Z"

        commits = self.get_paginated_results(commits_query, commits_params)
        total_commits = len(commits)

        # Handle date ranges properly for search queries
        date_filter = ""
        if start_date:
            date_filter += f"+created:>={start_date}"
        if end_date:
            date_filter += f"+created:<={end_date}"

        # Get all PRs created during the specified period
        prs_in_period_query = f"search/issues?q=repo:{owner}/{repo}+is:pr{date_filter}"
        prs_in_period = self.get_paginated_results(prs_in_period_query)

        # Count PRs that are still open
        open_prs_count = sum(1 for pr in prs_in_period if pr.get("state") == "open")

        # Extract PR numbers
        pr_numbers = []
        for item in prs_in_period:
            pr_url = item.get("pull_request", {}).get("url", "")
            match = re.search(r'/pulls/(\d+)$', pr_url)
            if match:
                pr_numbers.append(match.group(1))

        # Get reviews for each PR
        total_reviews = 0
        for pr_number in pr_numbers:
            reviews_endpoint = f"repos/{owner}/{repo}/pulls/{pr_number}/reviews"
            reviews = self.get_paginated_results(reviews_endpoint)

            # Filter reviews by date if needed
            if start_date or end_date:
                for review in reviews:
                    submitted_at = review.get("submitted_at", "")
                    if submitted_at:
                        review_date = submitted_at.split("T")[0]  # Extract YYYY-MM-DD part

                        # Only count if review is within the specified date range
                        if (not start_date or review_date >= start_date) and \
                                (not end_date or review_date <= end_date):
                            total_reviews += 1
            else:
                total_reviews += len(reviews)

        # Get all issues created during the specified period
        issues_in_period_query = f"search/issues?q=repo:{owner}/{repo}+is:issue{date_filter}"
        issues_in_period = self.get_paginated_results(issues_in_period_query)

        # Count issues that are still open
        active_issues_count = sum(1 for issue in issues_in_period if issue.get("state") == "open")

        return {
            "repository_name": repo_info["name"],
            "owner": repo_info["owner"]["login"],
            "total_commits": total_commits,
            "open_pull_requests": open_prs_count,
            "code_reviews": total_reviews,
            "active_issues": active_issues_count,
            "period": {
                "start_date": start_date,
                "end_date": end_date
            }
        }