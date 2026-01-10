# FastAPI Best Practices

Complete FastAPI patterns from [zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices).

## Project Structure - Domain-Driven

Domain-driven project structure inspired by Netflix's Dispatch. Store all domain directories inside `src` folder.

```
fastapi-project
├── alembic/
├── src
│   ├── auth
│   │   ├── router.py       # core endpoints
│   │   ├── schemas.py      # pydantic models
│   │   ├── models.py       # db models
│   │   ├── dependencies.py
│   │   ├── config.py
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   ├── service.py
│   │   └── utils.py
│   ├── posts
│   │   ├── router.py
│   │   ├── schemas.py
│   │   ├── models.py
│   │   └── ...
│   ├── config.py       # global configs
│   ├── models.py       # global models
│   ├── exceptions.py
│   ├── pagination.py
│   ├── database.py
│   └── main.py
├── tests/
├── templates/
└── requirements/
```

Import from other packages with explicit module names:

```python
from src.auth import constants as auth_constants
from src.notifications import service as notification_service
from src.posts.constants import ErrorCode as PostsErrorCode
```

---

## Async Routes

### I/O Intensive Tasks

FastAPI handles sync routes in threadpool, async routes on event loop. Never use blocking operations in async routes.

```python
# BAD - blocks event loop
@router.get("/terrible-ping")
async def terrible_ping():
    time.sleep(10)  # I/O blocking operation, whole process blocked
    return {"pong": True}

# GOOD - runs in threadpool
@router.get("/good-ping")
def good_ping():
    time.sleep(10)  # Blocking but in separate thread
    return {"pong": True}

# PERFECT - non-blocking async
@router.get("/perfect-ping")
async def perfect_ping():
    await asyncio.sleep(10)  # Non-blocking I/O
    return {"pong": True}
```

### CPU Intensive Tasks

CPU-intensive tasks should not be awaited or run in threadpool due to GIL. Send them to workers in another process.

### Sync SDK in Thread Pool

If you must use a library that's not async, use `run_in_threadpool`:

```python
from fastapi.concurrency import run_in_threadpool
from my_sync_library import SyncAPIClient

@app.get("/")
async def call_my_sync_library():
    my_data = await service.get_my_data()
    client = SyncAPIClient()
    await run_in_threadpool(client.make_request, data=my_data)
```

---

## Pydantic Patterns

### Excessively Use Pydantic

Pydantic has rich features for validation:

```python
from enum import Enum
from pydantic import AnyUrl, BaseModel, EmailStr, Field

class MusicBand(str, Enum):
   AEROSMITH = "AEROSMITH"
   QUEEN = "QUEEN"
   ACDC = "AC/DC"

class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=128)
    username: str = Field(min_length=1, max_length=128, pattern="^[A-Za-z0-9-_]+$")
    email: EmailStr
    age: int = Field(ge=18, default=None)
    favorite_band: MusicBand | None = None
    website: AnyUrl | None = None
```

### Custom Base Model

Create a controllable global base model:

```python
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict

def datetime_to_gmt_str(dt: datetime) -> str:
    if not dt.tzinfo:
        dt = dt.replace(tzinfo=ZoneInfo("UTC"))
    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")

class CustomModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: datetime_to_gmt_str},
        populate_by_name=True,
    )

    def serializable_dict(self, **kwargs):
        """Return a dict which contains only serializable fields."""
        default_dict = self.model_dump()
        return jsonable_encoder(default_dict)
```

### Decouple BaseSettings

Split BaseSettings across different modules:

```python
# src.auth.config
from pydantic_settings import BaseSettings

class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_SECRET: str
    JWT_EXP: int = 5  # minutes
    REFRESH_TOKEN_KEY: str
    SECURE_COOKIES: bool = True

auth_settings = AuthConfig()

# src.config
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    DATABASE_URL: PostgresDsn
    REDIS_URL: RedisDsn
    SITE_DOMAIN: str = "myapp.com"
    ENVIRONMENT: Environment = Environment.PRODUCTION

settings = Config()
```

### ValueError Becomes ValidationError

```python
from pydantic import BaseModel, field_validator

class ProfileCreate(BaseModel):
    username: str
    password: str

    @field_validator("password", mode="after")
    @classmethod
    def valid_password(cls, password: str) -> str:
        if not re.match(STRONG_PASSWORD_PATTERN, password):
            raise ValueError(
                "Password must contain at least "
                "one lower character, "
                "one upper character, "
                "digit or "
                "special symbol"
            )
        return password
```

---

## Dependencies

### Request Validation

Dependencies are excellent for request validation:

```python
# dependencies.py
async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()
    return post

# router.py
@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post_by_id(post: dict[str, Any] = Depends(valid_post_id)):
    return post

@router.put("/posts/{post_id}", response_model=PostResponse)
async def update_post(
    update_data: PostUpdate,
    post: dict[str, Any] = Depends(valid_post_id),
):
    updated_post = await service.update(id=post["id"], data=update_data)
    return updated_post
```

### Chain Dependencies

Dependencies can use other dependencies:

```python
async def valid_post_id(post_id: UUID4) -> dict[str, Any]:
    post = await service.get_by_id(post_id)
    if not post:
        raise PostNotFound()
    return post

async def parse_jwt_data(
    token: str = Depends(OAuth2PasswordBearer(tokenUrl="/auth/token"))
) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, "JWT_SECRET", algorithms=["HS256"])
    except JWTError:
        raise InvalidCredentials()
    return {"user_id": payload["id"]}

async def valid_owned_post(
    post: dict[str, Any] = Depends(valid_post_id),
    token_data: dict[str, Any] = Depends(parse_jwt_data),
) -> dict[str, Any]:
    if post["creator_id"] != token_data["user_id"]:
        raise UserNotOwner()
    return post
```

### Dependency Caching

FastAPI caches dependency's result within a request's scope by default:

```python
# parse_jwt_data is used 3 times but called only once
@router.get("/users/{user_id}/posts/{post_id}", response_model=PostResponse)
async def get_user_post(
    worker: BackgroundTasks,
    post: Mapping = Depends(valid_owned_post),  # uses parse_jwt_data
    user: Mapping = Depends(valid_active_creator),  # uses parse_jwt_data
):
    # parse_jwt_data is called only once, cached for this request
    worker.add_task(notifications_service.send_email, user["id"])
    return post
```

### Prefer Async Dependencies

Sync dependencies run in the thread pool. Prefer async for non-I/O operations.

---

## API Design

### Follow REST Conventions

Use consistent variable names in paths:

```python
@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(profile: Mapping = Depends(valid_profile_id)):
    return profile

@router.get("/creators/{profile_id}", response_model=ProfileResponse)
async def get_user_profile_by_id(
     creator_profile: Mapping = Depends(valid_creator_id)
):
    return creator_profile
```

### Hide Docs by Default

Unless your API is public:

```python
from fastapi import FastAPI
from starlette.config import Config

config = Config(".env")
ENVIRONMENT = config("ENVIRONMENT")
SHOW_DOCS_ENVIRONMENT = ("local", "staging")

app_configs = {"title": "My Cool API"}
if ENVIRONMENT not in SHOW_DOCS_ENVIRONMENT:
   app_configs["openapi_url"] = None

app = FastAPI(**app_configs)
```

### Detailed API Documentation

```python
from fastapi import APIRouter, status

@router.post(
    "/endpoints",
    response_model=DefaultResponseModel,
    status_code=status.HTTP_201_CREATED,
    description="Description of the well documented endpoint",
    tags=["Endpoint Category"],
    summary="Summary of the Endpoint",
    responses={
        status.HTTP_200_OK: {
            "model": OkResponse,
            "description": "Ok Response",
        },
        status.HTTP_201_CREATED: {
            "model": CreatedResponse,
            "description": "Creates something from user request",
        },
    },
)
async def documented_route():
    pass
```

---

## Testing

### Async Test Client from Day 0

Set the async test client immediately:

```python
import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.mark.asyncio
async def test_create_post(client: AsyncClient):
    resp = await client.post("/posts")
    assert resp.status_code == 201
```

---

## Tooling

### Use Ruff

Ruff is blazingly-fast linter that replaces black, autoflake, isort:

```bash
#!/bin/sh -e
set -x

ruff check --fix src
ruff format src
```

---

## Deslop - Remove Emojis

AI-generated code often includes emojis. Remove them:

```python
import re

def remove_emoji(text: str) -> str:
    """Remove emoji characters from text."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub("", text)
```
