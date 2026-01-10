---
name: error-handling
description: >
  Reliable error handling for Python APIs. Use when: (1) Designing error schemas,
  (2) Mapping exceptions to responses, (3) Logging failures consistently.
---

# error-handling

Progressive patterns for predictable errors and safe responses.

## Quick Start

- Define error schema (code, message, request_id)
- Centralize exception handling

## Core Patterns

1. **Domain exceptions**: explicit error classes
2. **Stable codes**: client-friendly error codes
3. **Safe messages**: no internals exposed

## Advanced

- Error translation layer for external services
- Observability hooks for exceptions

## Pitfalls

- Leaking stack traces
- Inconsistent error shapes
- Swallowing exceptions

## References

- `references/quickstart.md`
- `references/pitfalls.md`
