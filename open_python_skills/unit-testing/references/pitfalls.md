# Unit Testing Pitfalls

## Common Issues

- **Over-mocking**: tests pass but reality fails
- **Global state**: shared mutation across tests
- **Slow tests**: avoid I/O in unit tests
- **Flaky tests**: hidden randomness or time dependence

## Fix Patterns

- Mock behavior, not implementation
- Reset state via fixtures with scope control
- Use `freezegun` for time-dependent code
- Isolate external calls behind adapters
