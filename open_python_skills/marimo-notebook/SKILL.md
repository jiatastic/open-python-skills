---
name: marimo-notebook
description: >
  Reproducible notebooks with marimo. Use when: (1) Building reactive notebooks,
  (2) Shipping analysis as scripts/apps, (3) Exporting reports.
---

# marimo-notebook

Progressive patterns for building reliable marimo notebooks.

## Quick Start

- Install: `uv pip install marimo`
- Edit: `marimo edit notebook.py`
- Run: `marimo run notebook.py`

## Core Patterns

1. **Reactive cells**: let dependencies drive execution
2. **Deterministic runs**: avoid hidden state
3. **Exportable outputs**: HTML or script

## Advanced

- Parameterize via `mo.cli_args()`
- Gate expensive cells with `mo.stop()`
- Use `marimo export` for reports

## Pitfalls

- Hidden state from globals
- Expensive cells re-running
- Non-descriptive notebook names

## References

- `references/quickstart.md`
- `references/pitfalls.md`
