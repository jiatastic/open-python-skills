# Formatting Quickstart

## Black

```bash
uv pip install black
black .
```

## Ruff Format

```bash
uv pip install ruff
ruff format .
```

## Check without changing files

```bash
black --check .
ruff format --check .
```

## Pre-commit Hook

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.14.10
    hooks:
      - id: ruff-format
```
