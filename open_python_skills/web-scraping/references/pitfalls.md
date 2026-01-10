# Web Scraping Pitfalls

## Common Issues

- **Blocked requests**: missing headers or rate limits
- **Dynamic pages**: JS-rendered content not in HTML
- **Fragile selectors**: break on layout changes
- **Legal risk**: ignore robots.txt or ToS

## Fix Patterns

- Use `User-Agent` + delays
- Switch to Playwright for JS
- Prefer semantic selectors
- Store raw HTML snapshots
