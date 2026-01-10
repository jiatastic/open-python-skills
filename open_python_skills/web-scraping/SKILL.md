---
name: web-scraping
description: >
  Practical web scraping with requests, BeautifulSoup, and Playwright. Use when:
  (1) Extracting data from HTML, (2) Handling JS-rendered pages, (3) Building scrapers responsibly.
---

# web-scraping

Progressive scraping patterns for reliable data extraction.

## Quick Start

- Install: `uv pip install requests beautifulsoup4`
- Parse HTML with BeautifulSoup

## Core Patterns

1. **Stable selectors**: prefer semantic tags/attributes
2. **Polite scraping**: rate limits + `User-Agent`
3. **Robustness**: retries and timeouts
4. **Debuggable**: store raw HTML snapshots

## Advanced

- Playwright for JS-rendered pages
- Proxy rotation for high-volume scraping
- Structured extraction with schemas

## Pitfalls

- Ignoring robots.txt or ToS
- Brittle selectors tied to layout
- No backoff under rate limits

## References

- `references/quickstart.md`
- `references/pitfalls.md`
