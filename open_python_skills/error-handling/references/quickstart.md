# Error Handling Quickstart

## Patterns

- Define error types by domain
- Map exceptions to stable error codes
- Return consistent response shape

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

## Tip

Centralize exception handling in middleware or a base class.
