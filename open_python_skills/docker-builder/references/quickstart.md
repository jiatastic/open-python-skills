# Docker Builder Quickstart

## Minimal Dockerfile (FastAPI)

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install -U pip && pip install -e .
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Build & Run

```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
```

## Compose (Local)

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
```

## Multi-stage Example

```Dockerfile
# syntax=docker/dockerfile:1
FROM python:3.13-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
RUN python -m venv /app/venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-alpine
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/venv/bin:$PATH"
WORKDIR /app
COPY --from=builder /app/venv /app/venv
COPY . .
CMD ["python", "app.py"]
```
