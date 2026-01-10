# API Testing Pitfalls

## Common Issues

- **Schema mismatch**: OpenAPI not synced with runtime behavior
- **Auth failures**: missing headers or credentials
- **Flaky data**: non-idempotent endpoints break tests
- **Timeouts**: slow endpoints in CI

## Fix Patterns

- Generate schemas from code or validate schema updates
- Use `--header` or `--auth` for protected endpoints
- Isolate destructive endpoints into separate jobs
- Use `--phases examples` in smoke runs

## Example: Auth Header

```bash
schemathesis run https://api.example.com/openapi.json \
  --header "Authorization: Bearer $TOKEN"
```
