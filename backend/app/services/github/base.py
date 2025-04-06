import os
import logging
import requests
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class GitHubBaseService:
    """Base service for interacting with the GitHub API."""

    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {self.token}"
        }

    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make a request to the GitHub API."""

        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)

        if response.status_code != 200:
            logger.error(f"Error making request to {url}: {response.status_code} - {response.text}")
            response.raise_for_status()

        return response.json()

    def get_paginated_results(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """Get all results from a paginated GitHub API endpoint."""

        if params is None:
            params = {}

        # Set page size to maximum (100)
        params["per_page"] = 100

        # Initialize with first page
        all_results = []
        page = 1
        more_pages = True

        while more_pages:
            params["page"] = page
            url = f"{self.base_url}/{endpoint}"

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                logger.error(f"Error making request to {url}: {response.status_code} - {response.text}")
                response.raise_for_status()

            # Add results from this page
            page_results = response.json()

            # Handle different pagination formats
            if isinstance(page_results, list):
                if not page_results:  # Empty list means we've reached the end
                    more_pages = False
                all_results.extend(page_results)
            elif isinstance(page_results, dict) and "items" in page_results:
                # For search endpoints that return {items: [...], total_count: X}
                all_results.extend(page_results["items"])

                # Check if we've got all items
                if len(all_results) >= page_results.get("total_count", 0):
                    more_pages = False

            # Check for next link in headers
            if "Link" in response.headers:
                has_next = any(
                    'rel="next"' in link for link in response.headers["Link"].split(",")
                )
                if not has_next:
                    more_pages = False
            elif isinstance(page_results, list) and len(page_results) < params["per_page"]:
                # If we got fewer items than the max per page, we're on the last page
                more_pages = False

            page += 1

        return all_results