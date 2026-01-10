---
name: error-handling
description: >
  Reliable error handling for Python APIs. Use when: (1) Designing error schemas,
  (2) Mapping exceptions to responses, (3) Logging failures consistently.
---

# error-handling

Predictable error handling for API services, with stable schemas and centralized handlers.

## Overview

APIs should return consistent error shapes and stable codes. Use FastAPI's `HTTPException` and custom exception handlers to centralize logic.

## When to Use

- Designing client-consumable error responses
- Mapping domain exceptions to HTTP status codes
- Preventing stack trace leakage

## Quick Start (FastAPI)

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id != "42":
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
```

## Core Patterns

1. **Domain exceptions**: custom error classes per domain.
2. **Stable error codes**: machine-friendly values.
3. **Consistent shape**: `{"error": {"code": ..., "message": ...}}`.
4. **Central handlers**: one place to map exceptions.
5. **Safe messages**: avoid leaking internals.

## Custom Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse({"error": {"code": "http_error", "message": str(exc.detail)}}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse({"error": {"code": "validation_error", "message": "Invalid request"}}, status_code=400)
```

## Troubleshooting

- **Inconsistent codes**: define an enum or map
- **Leaked stack traces**: sanitize messages
- **Swallowed exceptions**: always log with context

## References

- https://fastapi.tiangolo.com/tutorial/handling-errors/
- https://fastapi.tiangolo.com/reference/exceptions/
