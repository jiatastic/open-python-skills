# Observability Quickstart

## Install Logfire

```bash
uv pip install logfire
```

## FastAPI Integration

```python
import logfire
from fastapi import FastAPI

app = FastAPI()
logfire.configure(service_name="backend")
logfire.instrument_fastapi(app)
logfire.instrument_httpx()
```

## Environment Variables

```bash
export LOGFIRE_SERVICE_NAME=backend
export LOGFIRE_ENVIRONMENT=production
```

## OTLP Exporter

```python
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

exporter = OTLPSpanExporter()
```
