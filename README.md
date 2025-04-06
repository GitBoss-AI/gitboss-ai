# GitBoss AI - Docker Setup

This document explains how to run GitBoss AI using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Start the Services

Run the following command in the root directory to start all services:

```bash
sudo docker compose up
```

This will start:
- Backend API server (FastAPI)

### 3. Access the Application

- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Stopping the Services

To stop all services:

```bash
docker-compose down
```

To stop and remove all containers, networks, and volumes:

```bash
docker-compose down -v
```