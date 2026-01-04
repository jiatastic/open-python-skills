# open-python-skills

An AI skill that provides intelligence for building solid Python backends across multiple platforms and frameworks.

## Overview

open-python-skills is a searchable knowledge database of FastAPI best practices, security patterns, database operations, Upstash integrations, deslopification guidelines, API design patterns, templates, and performance optimization techniques. It works as a skill/workflow for AI coding assistants (Claude Code, Cursor, Windsurf, etc.).

## Features

- **FastAPI Best Practices** - Project structure, dependency injection, async patterns, Pydantic models
- **Security & Authentication** - JWT/OAuth2, password hashing, API keys, CORS, rate limiting
- **Database Patterns** - SQLAlchemy 2.0, async operations, migrations, connection pooling
- **Upstash Integration** - Redis caching, session management, QStash background jobs, rate limiting
- **Deslopification** - AI code cleanup, refactoring patterns, naming conventions
- **API Design** - RESTful principles, versioning, pagination, response formats
- **Performance** - Caching strategies, async processing, profiling tools

## Quick Start

The skill activates automatically when you request backend development work. Just chat naturally:

```
Build a FastAPI REST API with JWT authentication

Create a caching layer using Upstash Redis

Refactor this AI-generated code to follow best practices
```

## Search Commands

```bash
# Search knowledge database
python3 .shared/scripts/knowledge_db.py "redis caching"

# Filter by category
python3 .shared/scripts/knowledge_db.py "async" --category upstash

# Get full entry with code examples
python3 .shared/scripts/knowledge_db.py --get upstash-fastapi-caching

# List all categories
python3 .shared/scripts/knowledge_db.py --list-categories

# List all tags
python3 .shared/scripts/knowledge_db.py --list-tags

# Show statistics
python3 .shared/scripts/knowledge_db.py --stats
```

## Available Categories

| Category | Entries | Description |
|----------|---------|-------------|
| `upstash` | 14 | Redis caching, rate limiting, QStash jobs |
| `performance` | 15 | Caching, pooling, async, profiling, streaming |
| `architecture` | 1 | Project structure, domain-driven design |
| `async` | 3 | Async/await patterns, event loop |
| `pydantic` | 4 | Validation, schemas, BaseSettings |
| `dependencies` | 4 | Dependency injection, chaining |
| `api` | 3 | REST conventions, documentation |
| `database` | 17 | SQLAlchemy, Alembic, ORM patterns, testing |
| `security` | 6 | JWT/OAuth2, password hashing, CORS |
| `template` | 1 | Project structure templates |
| `testing` | 1 | Async test client |
| `tooling` | 1 | Ruff, linting |
| `deslop` | 1 | AI code cleanup |

## Knowledge Databases

Located in `.shared/data/`:
- `fastapi_best_practices.json` - 23 curated FastAPI patterns
- `upstash_patterns.json` - 14 Redis/QStash integration patterns
- `security_patterns.json` - Auth/security patterns
- `database_patterns.json` - 17 SQLAlchemy/Alembic patterns
- `api_patterns.json` - API design patterns
- `perf_patterns.json` - 15 performance optimization patterns
- `template_patterns.json` - Project templates/scaffolding
- `deslop_patterns.json` - Code cleanup/deslopification patterns

Run `python3 .shared/scripts/knowledge_db.py --stats` to see the latest totals.
