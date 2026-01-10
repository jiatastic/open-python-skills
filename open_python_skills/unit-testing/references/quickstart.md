# Unit Testing Quickstart

## Minimal Setup

```bash
uv pip install pytest
```

## Project Layout

```
project/
├── src/
└── tests/
    ├── __init__.py
    └── test_example.py
```

## First Test

```python
# tests/test_example.py

def test_addition():
    assert 1 + 1 == 2
```

## Run

```bash
pytest -q
```

## Tips

- Keep tests small and focused
- Prefer `pytest` fixtures over custom setup code
