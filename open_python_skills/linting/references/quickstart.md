# Linting Quickstart

## Install

```bash
uv pip install ruff
```

## Run Lint

```bash
ruff check .
```

## Auto-fix

```bash
ruff check . --fix
```

## CI Output

```bash
ruff check . --output-format github
```

## Pre-commit Hook

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.10
    hooks:
      - id: ruff-check
      - id: ruff-format
```
