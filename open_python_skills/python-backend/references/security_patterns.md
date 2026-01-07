# Security Patterns

Authentication and security patterns for Python/FastAPI backends.

## Password Hashing (passlib + bcrypt)

Never store plaintext passwords. Hash with bcrypt:

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)
```

---

## JWT Create/Verify (python-jose)

Issue short-lived access tokens and validate them on each request:

```python
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

JWT_ALG = "HS256"
JWT_SECRET = "change-me"

def create_access_token(*, subject: str, expires_minutes: int = 15) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=expires_minutes)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except JWTError as e:
        raise ValueError("Invalid token") from e
```

---

## FastAPI OAuth2 Bearer Dependency

Use OAuth2PasswordBearer to parse `Authorization: Bearer <token>`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    return {"user_id": payload["sub"]}
```

---

## API Key Auth via Header

Protect internal endpoints with an API key header:

```python
from fastapi import Depends, Header, HTTPException, status

API_KEY = "change-me"

def require_api_key(
    x_api_key: str | None = Header(default=None, alias="X-API-Key")
) -> None:
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid API key"
        )
```

---

## CORS Configuration

Lock CORS down to known origins:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

---

## Hide OpenAPI Docs by Default

Disable docs endpoints in production:

```python
from fastapi import FastAPI

ENV = "production"  # e.g., from env vars

app = FastAPI(
    title="My API",
    openapi_url=None if ENV == "production" else "/openapi.json",
)
```
