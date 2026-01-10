---
name: docker-builder
description: >
  Build production-ready Docker images for Python APIs. Use when: (1) Creating Dockerfiles,
  (2) Optimizing image size, (3) Setting up compose for local dev.
---

# docker-builder

Progressive Docker patterns for Python APIs.

## Quick Start

- Build: `docker build -t my-api .`
- Run: `docker run -p 8000:8000 my-api`

## Core Patterns

1. **Multi-stage builds**: separate build/runtime
2. **Layer caching**: copy lock/config first
3. **Non-root runtime**: safer containers
4. **Signal handling**: use exec form CMD

## Advanced

- Distroless or slim images
- Buildkit cache mounts
- Healthchecks and readiness probes

## Pitfalls

- Large images with build deps
- Cache busting on every change
- Missing `PYTHONUNBUFFERED=1`

## References

- `references/quickstart.md`
- `references/pitfalls.md`
