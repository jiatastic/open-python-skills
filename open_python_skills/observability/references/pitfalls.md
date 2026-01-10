# Observability Pitfalls

## Common Issues

- **Missing service name**: traces are hard to find
- **No sampling config**: too much data in prod
- **Silent errors**: exceptions not captured

## Fix Patterns

- Set `LOGFIRE_SERVICE_NAME`
- Use sampling for high-traffic services
- Capture exceptions and error spans
