# Linting Quickstart

## Ruff Setup

```bash
uv pip install ruff
ruff check .
```

## Useful Commands

- Auto-fix: `ruff check . --fix`
- Format + lint: `ruff format . && ruff check .`

## Tip

Keep lint rules consistent with formatter to avoid churn.
