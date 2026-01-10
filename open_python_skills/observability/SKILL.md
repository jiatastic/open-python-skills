---
name: observability
description: >
  Observability with OpenTelemetry and Logfire. Use when: (1) Adding traces/logs to APIs,
  (2) Instrumenting FastAPI and httpx, (3) Setting up service metadata.
---

# observability

Structured observability patterns for Python APIs using Logfire and OpenTelemetry.

## Overview

Use Logfire for fast setup and OpenTelemetry for vendor-neutral exports. Always set service metadata, instrument key frameworks (FastAPI/httpx), and control sampling.

## When to Use

- Tracing API requests and dependencies
- Capturing structured logs with context
- Exporting telemetry to OTLP collectors

## Quick Start

```bash
uv pip install logfire
```

```python
import logfire
from fastapi import FastAPI

app = FastAPI()
logfire.configure(service_name="backend")
logfire.instrument_fastapi(app)
logfire.instrument_httpx()
```

## Core Patterns

1. **Service metadata**: set `service_name` and environment.
2. **Automatic instrumentation**: FastAPI + httpx for request spans.
3. **Structured logs**: include request IDs and user context.
4. **Sampling**: reduce volume for high-traffic services.
5. **OTLP exports**: keep backends swappable.

## OpenTelemetry Export Example

```python
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={"service.name": "service"})
trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

exporter = OTLPSpanExporter()
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(exporter))

with tracer.start_as_current_span("healthcheck"):
    pass
```

## Troubleshooting

- **Missing service name**: spans hard to find in UI
- **High-cardinality attributes**: explode storage
- **No spans**: instrumentation called too late

## References

- https://logfire.pydantic.dev/docs/
- https://opentelemetry.io/docs/instrumentation/python/
