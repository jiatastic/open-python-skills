---
name: docker-builder
description: >
  Build production-ready Docker images for Python APIs. Use when: (1) Creating Dockerfiles,
  (2) Optimizing image size, (3) Setting up compose for local dev.
---

# docker-builder

Production-grade Docker patterns for Python APIs with an emphasis on security and reproducibility.

## Overview

Use multi-stage builds, small base images, and deterministic installs to produce minimal, secure runtime images. Prioritize cache-friendly layer ordering and proper signal handling.

## When to Use

- Shipping FastAPI/Flask APIs to production
- Reducing image size and build times
- Standardizing container builds for teams

## Quick Start

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

## Core Patterns

1. **Multi-stage builds**: separate build and runtime stages.
2. **Layer caching**: copy lock files first.
3. **Virtualenv in image**: isolate dependencies.
4. **Non-root runtime**: reduce risk.
5. **Exec-form CMD**: proper signal handling.
6. **Healthchecks**: define liveness checks.

## Recommended Dockerfile (Multi-stage)

```Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
RUN python -m venv /app/venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-alpine
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /app/venv /app/venv
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Compose (Local Dev)

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

## Troubleshooting

- **Large images**: use multi-stage and avoid build deps in final stage
- **Slow builds**: maximize cache with lock-file-first ordering
- **Signal issues**: use exec-form `CMD` or `ENTRYPOINT`

## References

- https://docs.docker.com/build/building/best-practices/
- https://docs.docker.com/engine/
