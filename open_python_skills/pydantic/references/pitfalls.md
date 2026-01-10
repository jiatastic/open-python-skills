# Pydantic Pitfalls

## Common Issues

- **Silent coercion**: unexpected type casting
- **Slow validators**: heavy logic in validation
- **Mutable defaults**: shared state

## Fix Patterns

- Use strict types where needed
- Keep validators fast and simple
- Use `Field(default_factory=...)`

## Example: default_factory

```python
from pydantic import BaseModel, Field

class Model(BaseModel):
    tags: list[str] = Field(default_factory=list)
```
