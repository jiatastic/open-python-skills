---
name: unit-testing
description: >
  Practical unit testing with pytest. Use when: (1) Writing new tests, (2) Refactoring safely,
  (3) Fixing flaky tests, (4) Designing fixtures and mocks.
---

# unit-testing

Practical, production-ready testing patterns for Python projects using pytest.

## Overview

pytest makes it easy to write small, readable tests and scale to large suites. It provides plain `assert` statements, fixtures for dependency injection, parametrization, and a powerful plugin system.

## When to Use

- Adding unit tests for new code paths
- Refactoring with regression coverage
- Designing clean setup/teardown with fixtures
- Handling flaky tests with deterministic patterns

## When Not to Use

- End-to-end browser tests (use Playwright or Selenium)
- Non-Python services (use their native frameworks)

## Quick Start

```bash
uv pip install pytest
pytest
pytest tests/test_example.py -q
```

## Core Patterns

1. **Plain asserts**: pytest introspects failures without `self.assert*`.
2. **Fixtures**: reusable setup/teardown with `@pytest.fixture` and `yield`.
3. **Parametrization**: cover edge cases without duplication.
4. **Markers**: `@pytest.mark.slow`, `@pytest.mark.xfail`, `@pytest.mark.skipif`.
5. **Temporary paths**: `tmp_path` for filesystem-safe tests.
6. **Monkeypatching**: override env, functions, or paths safely.

## Configuration

Use `pyproject.toml` to standardize test discovery and markers:

```toml
[tool.pytest.ini_options]
minversion = "6.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
markers = [
  "slow: marks tests as slow",
  "integration: marks tests as integration tests",
  "unit: marks tests as unit tests",
]
addopts = ["-ra", "--strict-markers", "--strict-config"]
```

## Example: Fixtures with Teardown

```python
import pytest
import sqlite3

@pytest.fixture
def db(tmp_path):
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    yield conn
    conn.close()

def test_insert(db):
    cur = db.cursor()
    cur.execute("CREATE TABLE users (id INTEGER)")
    cur.execute("INSERT INTO users (id) VALUES (1)")
    db.commit()
    cur.execute("SELECT COUNT(*) FROM users")
    assert cur.fetchone()[0] == 1
```

## Example: Parametrization with Marks

```python
import pytest

@pytest.mark.parametrize(
    "value,expected",
    [
        (1, 2),
        pytest.param(1, 0, marks=pytest.mark.xfail),
        (2, 3),
    ],
)
def test_increment(value, expected):
    assert value + 1 == expected
```

## Example: tmp_path + monkeypatch

```python
def test_chdir(monkeypatch, tmp_path):
    subdir = tmp_path / "work"
    subdir.mkdir()
    monkeypatch.chdir(subdir)
    assert subdir.exists()
```

## Troubleshooting

- **Tests not collected**: confirm file names match `test_*.py` or `*_test.py`.
- **Unknown marker warnings**: register markers in config or enable `--strict-markers`.
- **Flaky tests**: remove randomness, fix time dependencies, avoid shared global state.

## References

- https://docs.pytest.org/en/stable/
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.pytest.org/en/stable/how-to/parametrize.html
- https://docs.pytest.org/en/stable/how-to/monkeypatch.html
