# Observability Quickstart

## Logfire + OpenTelemetry (Python)

```bash
uv pip install logfire
```

```python
import logfire

logfire.configure()
logfire.instrument_fastapi(app)
logfire.instrument_httpx()
```

## Environment Variables

```bash
export LOGFIRE_SERVICE_NAME=my_service
export LOGFIRE_ENVIRONMENT=production
```

## Tip

Use OpenTelemetry-compatible exporters so you can switch backends easily.
