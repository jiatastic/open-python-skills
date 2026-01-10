# Error Handling Pitfalls

## Common Issues

- **Leaking internals**: stack traces to clients
- **Inconsistent codes**: clients cannot branch reliably
- **Swallowed exceptions**: missing logs

## Fix Patterns

- Standardize error schema and codes
- Use central exception handlers
- Log with request context and IDs
