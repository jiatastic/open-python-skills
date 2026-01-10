---
name: marimo-notebook
description: >
  Reproducible notebooks with marimo. Use when: (1) Building reactive notebooks,
  (2) Shipping analysis as scripts/apps, (3) Exporting reports.
---

# marimo-notebook

Reproducible, reactive notebooks built as Python files with CLI and export support.

## Overview

Marimo notebooks are plain `.py` files with reactive execution. You can run them as scripts, apps, or export to HTML.

## When to Use

- Replacing Jupyter notebooks with deterministic execution
- Shipping analysis as a script or web app
- Exporting reports to HTML

## Quick Start

```bash
uv pip install marimo
marimo edit notebook.py
marimo run notebook.py
```

## Core Patterns

1. **Reactive cells**: dependency-based execution.
2. **No hidden state**: deterministic runs.
3. **CLI args**: parameterize runs with `mo.cli_args()`.
4. **Export**: `marimo export html` for reports.

## Example: CLI Args

```python
import marimo as mo

args = mo.cli_args()
name = args.get("name", "World")
mo.md(f"# Hello, {name}!")
```

## Example: Export

```bash
marimo export html notebook.py -o report.html -- --name Alice
```

## Troubleshooting

- **Hidden state**: avoid globals; rely on cell outputs
- **Expensive cells**: gate with `mo.stop()`
- **Naming**: use descriptive filenames for reuse

## References

- https://docs.marimo.io/
