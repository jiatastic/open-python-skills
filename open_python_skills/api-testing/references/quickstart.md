# API Testing Quickstart

## Install

```bash
uv pip install schemathesis
```

## Run Against Live Schema

```bash
schemathesis run https://api.example.com/openapi.json \
  --header "Authorization: Bearer $API_TOKEN"
```

## Run Against Local Schema

```bash
schemathesis run ./openapi.yaml --url https://api.example.com
```

## Common Options

- `--phases examples,fuzzing`
- `--workers 4`
- `--report junit --report-dir ./reports`
- `--seed 42` for reproducibility

## CI Example

```bash
schemathesis run ./openapi.yaml --url https://api.example.com \
  --report junit --report-dir ./reports
```
