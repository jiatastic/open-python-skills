# Formatting Pitfalls

## Common Issues

- **Multiple formatters** fighting each other
- **Inconsistent line length** across tools
- **Formatting only in CI** without local checks

## Fix Patterns

- Choose one formatter (Black or Ruff)
- Align line length in `pyproject.toml`
- Add pre-commit hooks for local enforcement

## Example: Black Config

```toml
[tool.black]
line-length = 88
```
