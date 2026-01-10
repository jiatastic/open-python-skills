# API Testing Quickstart (OpenAPI)

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

## Useful Options

- `--max-examples 200` for more coverage
- `--continue-on-failure` to keep going
- `--report junit --report-dir ./reports` for CI
