#!/usr/bin/env python3
"""Starter marimo notebook template."""

from __future__ import annotations

import importlib


mo = importlib.import_module("marimo")
app = mo.App()


@app.cell
def cell_title():
    title = "Hello marimo"
    return title,


@app.cell
def cell_markdown(mo, title):
    mo.md(f"# {title}")
    return


if __name__ == "__main__":
    app.run()
