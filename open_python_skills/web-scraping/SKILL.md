---
name: web-scraping
description: >
  Practical web scraping with requests, BeautifulSoup, and Playwright. Use when:
  (1) Extracting data from HTML, (2) Handling JS-rendered pages, (3) Building scrapers responsibly.
---

# web-scraping

Reliable scraping patterns for static HTML and JavaScript-rendered pages.

## Overview

Start with `requests` + BeautifulSoup for static pages. When content is rendered by JavaScript, switch to Playwright. Always use timeouts, retries, and explicit user-agent headers.

## When to Use

- Extracting structured data from HTML pages
- Monitoring content changes
- Handling SPAs or dynamic content with a headless browser

## When Not to Use

- The site forbids scraping in ToS/robots.txt
- An official API is available (prefer it)

## Quick Start

```bash
uv pip install requests beautifulsoup4
```

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com", timeout=10)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
print(soup.title.text)
```

## Core Patterns

1. **Use a Session**: reuse connections and set default headers.
2. **Always set timeouts**: avoid hanging requests.
3. **Respect robots.txt/ToS**: throttle and avoid sensitive paths.
4. **Stable selectors**: prefer semantic attributes or ids.
5. **Capture HTML snapshots**: store responses for debugging.
6. **Escalate to Playwright**: for JS-rendered pages.

## Requests Patterns

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

session = requests.Session()
session.headers.update({"User-Agent": "my-scraper/1.0"})

retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

resp = session.get("https://example.com", timeout=10)
resp.raise_for_status()
```

## BeautifulSoup Patterns

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# CSS selectors
links = soup.select("a[href]")
main = soup.select_one("#main")
```

## Playwright (Dynamic Pages)

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com", wait_until="domcontentloaded")
    page.wait_for_selector(".product")
    html = page.content()
    browser.close()
```

## Troubleshooting

- **Blocked requests**: set `User-Agent`, add backoff, reduce rate.
- **Empty HTML**: page is JS-rendered; use Playwright.
- **Selector breakage**: update CSS selectors to stable attributes.

## References

- https://docs.python-requests.org/en/latest/
- https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- https://playwright.dev/python/
