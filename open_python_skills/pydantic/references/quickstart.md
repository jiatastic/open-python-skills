# Pydantic Quickstart

## Install

```bash
uv pip install pydantic
```

## Minimal Model

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    age: int
```

## Validation

```python
user = User(email="a@example.com", age=30)
```
