# Web Scraping Quickstart

## Basic Stack

```bash
uv pip install requests beautifulsoup4
```

## Minimal Example

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com")
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")
print(soup.title.text)
```

## Tips

- Respect robots.txt
- Add timeouts and retries
- Cache HTML for debugging
