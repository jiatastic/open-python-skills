---
name: api-testing
description: >
  OpenAPI-driven API testing with schemathesis. Use when: (1) Validating OpenAPI schemas,
  (2) Fuzzing endpoints, (3) Running API tests in CI.
---

# api-testing

Progressive API testing with OpenAPI schemas and schemathesis.

## Quick Start

- Install: `uv pip install schemathesis`
- Run: `schemathesis run ./openapi.yaml --url https://api.example.com`

## Core Patterns

1. **Schema-first**: keep OpenAPI synced to code
2. **Auth headers**: pass tokens in CLI/config
3. **CI reports**: JUnit output for pipelines
4. **Safe coverage**: avoid destructive endpoints by tag

## Advanced

- Phases: `--phases examples,fuzzing`
- Rate limiting: `--rate-limit 100/m`
- Reproducible runs: `--seed 42`

## Pitfalls

- Stale schemas causing false failures
- Unbounded fuzzing without timeouts
- Flaky endpoints with nondeterministic data

## References

- `references/quickstart.md`
- `references/pitfalls.md`
