---
name: python-backend
description: >
  Python backend development expertise for FastAPI, security patterns, database operations,
  Upstash integrations, and code quality. Use when: (1) Building REST APIs with FastAPI,
  (2) Implementing JWT/OAuth2 authentication, (3) Setting up SQLAlchemy/async databases,
  (4) Integrating Redis/Upstash caching, (5) Refactoring AI-generated Python code (deslopification),
  (6) Designing API patterns, or (7) Optimizing backend performance.
---

# python-backend

Searchable knowledge base for building production-ready Python backends.

## Search Usage

```bash
# Search knowledge database
python3 .shared/scripts/knowledge_db.py "{query}"

# Filter by category
python3 .shared/scripts/knowledge_db.py "{query}" --category {category}

# Get full entry with code examples
python3 .shared/scripts/knowledge_db.py --get {entry-id}

# List all categories
python3 .shared/scripts/knowledge_db.py --list-categories

# List all tags
python3 .shared/scripts/knowledge_db.py --list-tags
```

## Available Categories

- `architecture` - Project structure, domain-driven design
- `async` - Async/await patterns, event loop, threadpool
- `pydantic` - Validation, schemas, BaseSettings
- `dependencies` - Dependency injection, chaining, caching
- `api` - REST conventions, documentation
- `database` - SQLAlchemy, naming conventions, migrations
- `testing` - Async test client, pytest
- `tooling` - Ruff, linting, formatting
- `upstash` - Redis caching, rate limiting, QStash jobs
- `security` - JWT/OAuth2, password hashing, API keys, CORS
- `template` - Project templates, architecture scaffolding
- `deslop` - AI code cleanup, refactoring

## Knowledge Databases

Located in `.shared/data/` (loaded automatically by `knowledge_db.py`):
- `fastapi_best_practices.json` - FastAPI patterns
- `upstash_patterns.json` - Redis/QStash integration
- `security_patterns.json` - Auth/security patterns
- `database_patterns.json` - SQLAlchemy/Alembic patterns
- `api_patterns.json` - API design patterns
- `perf_patterns.json` - Performance patterns
- `template_patterns.json` - Project templates
- `deslop_patterns.json` - Code cleanup patterns

## Core Principles

1. **Async-first** - Use async/await for I/O operations
2. **Type everything** - Pydantic models for validation
3. **Dependency injection** - Use FastAPI's Depends()
4. **Fail fast** - Validate early, use HTTPException
5. **Security by default** - Never trust user input
