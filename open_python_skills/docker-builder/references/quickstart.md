# Docker Builder Quickstart

## Minimal Dockerfile (FastAPI)

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml ./
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
