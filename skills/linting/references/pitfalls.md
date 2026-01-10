# Linting Pitfalls

## Common Issues

- **Conflicting tools**: formatter vs linter rules
- **Overly strict rules**: high noise, low adoption
- **Excessive ignores**: hides real issues

## Fix Patterns

- Align linter with formatter defaults
- Start with `E` and `F`, expand later
- Keep ignores local and documented

## Example: Reduce Noise

```toml
[tool.ruff.lint]
select = ["E", "F"]
ignore = ["E501"]
```
