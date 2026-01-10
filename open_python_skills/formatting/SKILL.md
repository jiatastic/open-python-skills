---
name: formatting
description: >
  Code formatting with black or ruff-format. Use when: (1) Standardizing code style,
  (2) Reducing review noise, (3) Enforcing formatting in CI.
---

# formatting

Opinionated formatting for Python codebases using Black or Ruff Format.

## Overview

Pick a single formatter for the entire project. Black is the classic choice; Ruff Format is faster and integrates with Ruff.

## When to Use

- Standardizing style across a team
- Reducing review noise
- Enforcing format checks in CI

## Quick Start

```bash
uv pip install black
black .
```

or

```bash
uv pip install ruff
ruff format .
```

## Configuration (Black)

```toml
[tool.black]
line-length = 88
target-version = ["py310", "py311"]
include = "\\.pyi?$"
extend-exclude = """
/(\.venv|dist|build)/
"""
```

## Configuration (Ruff Format)

```toml
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

## Best Practices

1. **One formatter only**: avoid tool fights.
2. **Run locally**: do not rely only on CI.
3. **Pre-commit integration**: catch format issues early.
4. **Dedicated formatting commits**: reduce review noise.

## Troubleshooting

- **Conflicts**: remove other formatters.
- **Line length churn**: align line length across tools.

## References

- https://black.readthedocs.io/en/stable/
- https://docs.astral.sh/ruff/formatter/
