---
name: open-python-skills
description: >
  Python backend development expertise for FastAPI, security patterns, database operations,
  Upstash integrations, and code quality. Use when: (1) Building REST APIs with FastAPI,
  (2) Implementing JWT/OAuth2 authentication, (3) Setting up SQLAlchemy/async databases,
  (4) Integrating Redis/Upstash caching, (5) Refactoring AI-generated Python code (deslopification),
  (6) Designing API patterns, or (7) Optimizing backend performance.
---

# Python Backend Pro Max

Searchable knowledge base for building production-ready Python backends.

## Search Usage

```bash
# Search reference documents
python3 scripts/search.py "{query}" --domain {domain}

# Search knowledge database  
python3 scripts/knowledge_db.py "{query}"

# Get full entry with code examples
python3 scripts/knowledge_db.py --get {entry-id}
```

## Available Domains

- `fastapi` - Project structure, DI, async patterns, Pydantic
- `security` - JWT, OAuth2, password hashing, API keys, CORS
- `database` - SQLAlchemy 2.0, async operations, migrations
- `upstash` - Redis caching, QStash background jobs
- `deslop` - AI code cleanup, refactoring patterns
- `api` - REST patterns, versioning, pagination
- `perf` - Caching, profiling, optimization
- `template` - Project templates, architectures

## Reference Documents

Located in `references/`:
- fastapi.md, security.md, database.md, upstash.md
- deslop.md, api.md, perf.md, template.md

## Knowledge Database

- `data/fastapi_best_practices.json` - 21 curated entries

## Core Principles

1. **Async-first** - Use async/await for I/O operations
2. **Type everything** - Pydantic models for validation
3. **Dependency injection** - Use FastAPI's Depends()
4. **Fail fast** - Validate early, use HTTPException
5. **Security by default** - Never trust user input
