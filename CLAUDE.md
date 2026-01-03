# Python Backend Pro Max

This is an AI skill that provides intelligence for building solid Python backends.

## Quick Start

When working on Python backend tasks, use the search tool:

```bash
python3 .shared/py-backend-pro/scripts/search.py "<query>" --domain <domain>
```

## Available Domains

- `fastapi` - FastAPI best practices
- `security` - Authentication, authorization, security
- `database` - SQLAlchemy, async DB, migrations
- `upstash` - Redis caching, QStash, Kafka
- `deslop` - Deslopification (AI code cleanup)
- `api` - API design patterns
- `template` - Project templates
- `perf` - Performance optimization

## Example Usage

```bash
# Search for dependency injection patterns
python3 .shared/py-backend-pro/scripts/search.py "dependency injection" --domain fastapi

# Search for JWT authentication
python3 .shared/py-backend-pro/scripts/search.py "JWT authentication" --domain security

# Search for caching strategies
python3 .shared/py-backend-pro/scripts/search.py "caching redis" --domain upstash
```
