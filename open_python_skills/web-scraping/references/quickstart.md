# Web Scraping Quickstart

## Install

```bash
uv pip install requests beautifulsoup4
```

## Minimal Example

```python
import requests
from bs4 import BeautifulSoup

resp = requests.get("https://example.com", timeout=10)
resp.raise_for_status()

soup = BeautifulSoup(resp.text, "html.parser")
print(soup.title.text)
```

## Requests Session + Retry

```python
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

session = Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

resp = session.get("https://example.com", timeout=10)
```

## CSS Selectors

```python
soup.select("a[href]")
soup.select_one("#main")
```

## Playwright for JS

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://example.com", wait_until="domcontentloaded")
    page.wait_for_selector(".content")
    html = page.content()
    browser.close()
```
