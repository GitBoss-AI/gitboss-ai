# GitBoss AI - API Documentation

This document outlines the available endpoints for the GitBoss AI backend.

## Base URL

All endpoints are relative to the base URL: `http://localhost:8000`

## Health Check

### `GET /api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "ok"
}
```

## Repository Stats

### `GET /api/repos/{owner}/{repo}/stats`

Get repository statistics for a specific time period.

**Parameters:**
- `owner` (path): Repository owner
- `repo` (path): Repository name
- `start_date` (query, optional): Start date in YYYY-MM-DD format
- `end_date` (query, optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "repository_name": "rich-cli",
  "owner": "Textualize",
  "total_commits": 109,
  "open_pull_requests": 13,
  "code_reviews": 19,
  "active_issues": 22,
  "period": {
    "start_date": "2023-01-01",
    "end_date": "2023-12-31"
  }
}
```

## Contributors

### `GET /api/contributors/{owner}/{repo}`

Get repository contributors with their statistics.

**Parameters:**
- `owner` (path): Repository owner
- `repo` (path): Repository name
- `start_date` (query, optional): Start date in YYYY-MM-DD format
- `end_date` (query, optional): End date in YYYY-MM-DD format

**Response:**
```json
[
  {
    "username": "willmcgugan",
    "avatar_url": "https://avatars.githubusercontent.com/u/554369?v=4",
    "commits": 87,
    "pull_requests": 0,
    "reviews": 0,
    "total_contributions": 87,
    "recent_activity": [
      {
        "type": "commit",
        "repo": "rich-cli",
        "details": {
          "sha": "abc1234",
          "message": "Fix bug in rendering"
        },
        "timestamp": "2023-04-01T12:34:56Z"
      }
    ]
  }
]
```

### `GET /api/contributors/{owner}/{repo}/weekly`

Get weekly statistics for each contributor.

**Parameters:**
- `owner` (path): Repository owner
- `repo` (path): Repository name
- `weeks` (query, optional): Number of weeks to include (default: 4)

**Response:**
```json
{
  "willmcgugan": {
    "username": "willmcgugan",
    "avatar_url": "https://avatars.githubusercontent.com/u/554369?v=4",
    "weekly_data": [
      {
        "week": "W1",
        "week_start": "2023-03-05",
        "week_end": "2023-03-12",
        "commits": 15,
        "pull_requests": 3,
        "reviews": 5
      },
      {
        "week": "W2",
        "week_start": "2023-03-12",
        "week_end": "2023-03-19",
        "commits": 12,
        "pull_requests": 2,
        "reviews": 4
      }
    ]
  }
}
```

## WebSocket

### `WebSocket /ws/chat`

Connect to the WebSocket chat service.

**Messages sent to server format:**
```json
{
  "message": "Who worked on PR #123?"
}
```

**Messages received from server format:**
```json
{
  "type": "response",
  "message": "PR #123 was worked on by @username"
}
```

## Rate Limiting Note

The GitHub API has rate limits. If you encounter 403 errors with messages about rate limits being exceeded, you may need to wait before making additional requests.