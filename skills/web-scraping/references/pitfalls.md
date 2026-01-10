# Web Scraping Pitfalls

## Common Issues

- **Blocked requests**: missing user-agent, aggressive rate
- **Dynamic pages**: HTML is empty or incomplete
- **Fragile selectors**: break on layout changes
- **Legal/ToS**: ignore robots.txt or site policy

## Fix Patterns

- Set headers and add delays/backoff
- Switch to Playwright for JS-rendered pages
- Prefer semantic selectors and IDs
- Archive HTML to debug changes

## Example: Headers + Timeout

```python
resp = requests.get(
    "https://example.com",
    headers={"User-Agent": "my-scraper/1.0"},
    timeout=10,
)
```
