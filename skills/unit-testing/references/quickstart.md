# Unit Testing Quickstart

## Install

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
pytest
pytest -q
pytest tests/test_example.py
```

## Useful Flags

- `-k "pattern"` to run a subset
- `-m "not slow"` to filter by markers
- `-x` to stop at first failure
- `-ra` to show extra test summary info

## Common Test Patterns

```python
import pytest

@pytest.mark.parametrize("x,expected", [(1, 2), (2, 3)])
def test_increment(x, expected):
    assert x + 1 == expected


def test_exception():
    with pytest.raises(ValueError):
        int("not-a-number")
```
