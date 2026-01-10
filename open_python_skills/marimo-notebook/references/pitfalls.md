# marimo Pitfalls

## Common Issues

- **Hidden state**: globals or side effects
- **Expensive cells**: rerun too often
- **Unnamed notebooks**: unclear dependency graphs

## Fix Patterns

- Use explicit outputs between cells
- Gate expensive work with `mo.stop()`
- Keep notebooks small and well-named
