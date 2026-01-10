# marimo Pitfalls

## Common Issues

- **Hidden state**: avoid globals, prefer cell outputs
- **Expensive cells**: re-run too often
- **Inconsistent names**: hard to trace dependencies

## Fix Patterns

- Use explicit outputs from cells
- Gate expensive work with `mo.stop()`
- Keep descriptive file names
