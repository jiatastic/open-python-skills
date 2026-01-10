# Error Handling Pitfalls

## Common Issues

- **Leaking internals**: stack traces to clients
- **Inconsistent codes**: hard to handle on client
- **Swallowed exceptions**: silent failures

## Fix Patterns

- Use safe error messages
- Define a single error schema
- Log exceptions with context
