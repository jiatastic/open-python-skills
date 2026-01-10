---
name: observability
description: >
  Observability with OpenTelemetry and Logfire. Use when: (1) Adding traces/logs to APIs,
  (2) Instrumenting FastAPI and httpx, (3) Setting up service metadata.
---

# observability

Progressive observability patterns for Python APIs.

## Quick Start

- Install: `uv pip install logfire`
- Configure and instrument FastAPI/httpx

## Core Patterns

1. **Service metadata**: set service name and environment
2. **Tracing first**: capture requests and dependencies
3. **Structured logging**: add context fields

## Advanced

- Sampling for high traffic
- Custom spans for critical paths
- OpenTelemetry exporters for portability

## Pitfalls

- Missing service name or env
- High-cardinality attributes
- Silent exceptions with no spans

## References

- `references/quickstart.md`
- `references/pitfalls.md`
