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

user = User(email="a@example.com", age=30)
```

## Serialization

```python
user.model_dump()
user.model_dump_json()
```

## Validators

```python
from pydantic import field_validator

class User(BaseModel):
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int):
        if v < 0:
            raise ValueError("age must be >= 0")
        return v
```
