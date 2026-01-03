# Python Backend Pro Max

An AI skill that provides intelligence for building solid Python backends across multiple platforms and frameworks.

## Overview

Python Backend Pro Max is a searchable database of FastAPI best practices, security patterns, database operations, Upstash integrations, deslopification guidelines, API design patterns, and performance optimization techniques. It works as a skill/workflow for AI coding assistants (Claude Code, Cursor, Windsurf, etc.).

## Features

- **FastAPI Best Practices** - Project structure, dependency injection, async patterns, Pydantic models
- **Security & Authentication** - JWT/OAuth2, password hashing, API keys, CORS, rate limiting
- **Database Patterns** - SQLAlchemy 2.0, async operations, migrations, connection pooling
- **Upstash Integration** - Redis caching, session management, QStash background jobs
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

### Reference Documents
```bash
python3 .shared/open-python-skills/scripts/search.py "jwt authentication" --domain security
python3 .shared/open-python-skills/scripts/search.py "dependency injection" --domain fastapi
python3 .shared/open-python-skills/scripts/search.py "redis caching" --domain upstash
python3 .shared/open-python-skills/scripts/search.py "naming conventions" --domain deslop
```

### Knowledge Database (FastAPI Best Practices)
```bash
python3 .shared/open-python-skills/scripts/knowledge_db.py "async routes"
python3 .shared/open-python-skills/scripts/knowledge_db.py "pydantic" --category pydantic
python3 .shared/open-python-skills/scripts/knowledge_db.py --get async-routes-io
python3 .shared/open-python-skills/scripts/knowledge_db.py --list-categories
```

## Available Domains

| Domain | Description |
|--------|-------------|
| `fastapi` | FastAPI framework best practices |
| `security` | Authentication, authorization, security patterns |
| `database` | Database operations and ORM patterns |
| `upstash` | Upstash Redis, QStash, Kafka integration |
| `deslop` | Deslopification - AI code cleanup guidelines |
| `api` | API design patterns and conventions |
| `perf` | Performance optimization techniques |
| `template` | Project templates and architectures |
