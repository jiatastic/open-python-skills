#!/usr/bin/env python3
"""Minimal scraper example using requests + BeautifulSoup."""

from __future__ import annotations

import importlib
import sys
from typing import Iterable


def _import_or_exit(module_name: str, install_hint: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        raise SystemExit(install_hint) from exc


requests = _import_or_exit("requests", "Install requests: uv pip install requests")
bs4 = _import_or_exit("bs4", "Install BeautifulSoup: uv pip install beautifulsoup4")


def extract_links(html: str) -> Iterable[str]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    for link in soup.select("a[href]"):
        yield link.get("href", "")


def main(url: str) -> None:
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    for href in extract_links(response.text):
        if href:
            print(href)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: scrape_example.py <url>")
    main(sys.argv[1])
