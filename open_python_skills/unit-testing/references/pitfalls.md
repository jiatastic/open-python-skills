# Unit Testing Pitfalls

## Common Issues

- **Over-mocking**: tests pass but production fails
- **Global state**: shared mutation across tests
- **Slow tests**: I/O in unit tests slows the suite
- **Flaky tests**: hidden randomness or time dependence
- **Unregistered markers**: `PytestUnknownMarkWarning`

## Fix Patterns

- Mock boundaries, not internal details
- Use fixtures to isolate setup and teardown
- Prefer `tmp_path` for filesystem operations
- Remove randomness or fix the seed
- Register markers in `pyproject.toml`

## Fixture Scope Mistakes

- `scope="session"` can leak state across tests
- Use `function` scope by default and widen only when needed

## Example: Fix Flaky Time

```python
import time

def now_epoch():
    return int(time.time())

# Use a library like freezegun or inject time as a dependency
```
