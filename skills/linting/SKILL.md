---
name: linting
description: >
  Python linting with ruff. Use when: (1) Standardizing code quality,
  (2) Fixing style warnings, (3) Enforcing rules in CI.
---

# linting

Fast, opinionated linting with Ruff, designed as a drop-in replacement for Flake8 and friends.

## Overview

Ruff provides a single CLI for linting with optional auto-fix. It supports an extensive rule set and integrates cleanly with pre-commit and CI.

## When to Use

- Standardizing code quality
- Enforcing consistent rules in CI
- Replacing multiple tools (flake8, isort, pyupgrade)

## Quick Start

```bash
uv pip install ruff
ruff check .
```

## Core Patterns

1. **Start minimal**: enable `E` and `F`, then expand.
2. **Auto-fix**: use `ruff check --fix` for safe rules.
3. **Per-file ignores**: use sparingly for generated code.
4. **CI integration**: `ruff check --output-format github`.
5. **Single source of truth**: configure via `pyproject.toml`.

## Configuration (pyproject.toml)

```toml
[tool.ruff]
line-length = 88
target-version = "py311"
exclude = [".venv", "dist", "build"]

[tool.ruff.lint]
select = ["E", "F", "B", "I", "UP", "SIM"]
ignore = ["E501"]
fixable = ["ALL"]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101"]
```

## Useful Commands

```bash
ruff check .
ruff check . --fix
ruff check . --diff
ruff check . --output-format github
```

## Troubleshooting

- **Rule conflicts**: align with formatter rules.
- **Too strict**: start with small `select` list.
- **Too many ignores**: use per-file ignores sparingly.

## References

- https://docs.astral.sh/ruff/
