---
name: api-testing
description: >
  OpenAPI-driven API testing with schemathesis. Use when: (1) Validating OpenAPI schemas,
  (2) Fuzzing endpoints, (3) Running API tests in CI.
---

# api-testing

OpenAPI-driven API testing with Schemathesis for schema validation, fuzzing, and CI reporting.

## Overview

Schemathesis reads OpenAPI schemas (local or remote) and generates tests that validate API behavior. It supports authentication, different phases (examples and fuzzing), concurrency, and test reports.

## When to Use

- You already have OpenAPI specs and want coverage
- You need fuzzing or schema-driven tests
- You want CI-friendly reports (JUnit)

## When Not to Use

- No schema exists (generate one first)
- You need UI/browser tests

## Quick Start

```bash
uv pip install schemathesis
schemathesis run https://api.example.com/openapi.json
schemathesis run ./openapi.yaml --url https://api.example.com
```

## Core Patterns

1. **Schema-first**: keep OpenAPI synced to code.
2. **Auth headers**: pass tokens for protected endpoints.
3. **Phases**: use `--phases examples,fuzzing`.
4. **Concurrency**: scale with `--workers`.
5. **Rate limits**: throttle with config `rate-limit`.
6. **CI reports**: `--report junit --report-dir ./reports`.
7. **Reproducible runs**: set `--seed`.

## CLI Examples

```bash
# Auth header
schemathesis run https://api.example.com/openapi.json \
  --header "Authorization: Bearer $TOKEN"

# Examples + fuzzing
schemathesis run ./openapi.yaml --url https://api.example.com \
  --phases examples,fuzzing

# Concurrency
schemathesis run ./openapi.yaml --url https://api.example.com --workers 4

# JUnit report
schemathesis run ./openapi.yaml --url https://api.example.com \
  --report junit --report-dir ./reports
```

## Configuration

Use config to rate-limit tests:

```toml
rate-limit = "100/m"
```

## Troubleshooting

- **Schema mismatch**: regenerate OpenAPI from code
- **Auth failures**: confirm headers or basic auth
- **Flaky endpoints**: isolate destructive endpoints
- **Slow runs**: limit phases or reduce workers

## References

- https://schemathesis.readthedocs.io/
- https://github.com/schemathesis/schemathesis
