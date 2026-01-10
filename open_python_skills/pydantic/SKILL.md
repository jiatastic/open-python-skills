---
name: pydantic
description: >
  Pydantic models and validation. Use when: (1) Defining schemas,
  (2) Validating input/output, (3) Generating JSON schema.
---

# pydantic

Progressive patterns for modeling and validation with Pydantic.

## Quick Start

- Install: `uv pip install pydantic`
- Define `BaseModel` schemas

## Core Patterns

1. **Typed fields**: prefer strict types
2. **Validation**: use validators for custom rules
3. **Serialization**: `model_dump()` for output

## Advanced

- `@field_validator` for complex constraints
- Settings models for configuration
- JSON schema generation for docs

## Pitfalls

- Unintended coercion
- Mutable defaults without factories

## References

- `references/quickstart.md`
- `references/pitfalls.md`
