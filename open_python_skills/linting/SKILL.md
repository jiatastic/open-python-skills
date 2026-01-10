---
name: linting
description: >
  Python linting with ruff. Use when: (1) Standardizing code quality,
  (2) Fixing style warnings, (3) Enforcing rules in CI.
---

# linting

Progressive linting patterns with ruff.

## Quick Start

- Install: `uv pip install ruff`
- Run: `ruff check .`

## Core Patterns

1. **Fast feedback**: run in pre-commit or CI
2. **Auto-fix**: use `--fix` for safe rules
3. **Rule scoping**: start minimal, expand gradually

## Advanced

- Per-file ignores for generated code
- Rule presets for security and complexity

## Pitfalls

- Conflicting formatter/linter rules
- Excessive ignores that hide issues

## References

- `references/quickstart.md`
- `references/pitfalls.md`
