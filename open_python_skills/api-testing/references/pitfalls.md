# API Testing Pitfalls

## Common Issues

- **Schema mismatch**: OpenAPI not synced with code
- **Auth failures**: missing headers or tokens
- **Slow endpoints**: timeouts in CI
- **Flaky data**: non-idempotent endpoints

## Fix Patterns

- Generate schema from code when possible
- Use `--header` for auth in CLI/config
- Set `--request-timeout` and `--max-response-time`
- Split destructive endpoints into separate jobs
