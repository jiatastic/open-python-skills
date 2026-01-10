# Error Handling Quickstart

## Patterns

- Define domain error classes
- Map exceptions to status codes
- Return a stable error shape

## Example Response

```json
{
  "error": {
    "code": "user_not_found",
    "message": "User not found",
    "request_id": "..."
  }
}
```

## FastAPI Example

```python
from fastapi import HTTPException

if not user:
    raise HTTPException(status_code=404, detail="User not found")
```
