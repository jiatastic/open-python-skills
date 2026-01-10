# Pydantic Pitfalls

## Common Issues

- **Silent coercion**: unexpected type casting
- **Heavy validators**: slow model creation
- **Nested defaults**: mutable defaults

## Fix Patterns

- Use strict types where needed
- Keep validators fast
- Use `Field(default_factory=...)`
