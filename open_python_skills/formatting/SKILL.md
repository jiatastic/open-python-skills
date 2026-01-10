---
name: formatting
description: >
  Code formatting with black or ruff-format. Use when: (1) Standardizing code style,
  (2) Reducing review noise, (3) Enforcing formatting in CI.
---

# formatting

Progressive formatting patterns for Python codebases.

## Quick Start

- `black .` or `ruff format .`

## Core Patterns

1. **Single formatter**: avoid tool conflicts
2. **Consistent line length**: match editor/CI
3. **Pre-commit integration**: fast feedback

## Advanced

- Format-only changes in dedicated commits
- Format check in CI

## Pitfalls

- Mixing formatters with different rules
- Running format only in CI

## References

- `references/quickstart.md`
- `references/pitfalls.md`
