# Docker Builder Pitfalls

## Common Issues

- **Large images**: avoid installing build deps in final stage
- **Slow builds**: reorder layers to maximize cache hits
- **Permission errors**: run as non-root
- **Broken signals**: ensure process handles SIGTERM

## Fix Patterns

- Use multi-stage builds
- Copy only lock/config first
- Add `USER` for runtime
- Use `exec` form CMD
