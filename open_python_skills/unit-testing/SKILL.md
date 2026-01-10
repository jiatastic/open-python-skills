---
name: unit-testing
description: >
  Practical unit testing with pytest. Use when: (1) Writing new tests, (2) Refactoring safely,
  (3) Fixing flaky tests, (4) Designing fixtures and mocks.
---

# unit-testing

Progressive testing patterns for Python projects using pytest.

## Quick Start

- Install: `uv pip install pytest`
- Run all tests: `pytest`
- Run one file: `pytest tests/test_example.py`

## Core Patterns

1. **Test structure**: Arrange → Act → Assert
2. **Fixtures**: centralize setup/teardown
3. **Parametrization**: cover edge cases efficiently
4. **Mocking**: mock boundaries, not internals

## Advanced

- `hypothesis` for property-based testing
- `freezegun` for time-dependent code
- `pytest-xdist` for parallel runs

## Pitfalls

- Over-mocking implementation details
- Shared mutable state between tests
- Slow unit tests that perform I/O

## References

- `references/quickstart.md`
- `references/pitfalls.md`
