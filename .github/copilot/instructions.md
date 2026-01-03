# GitHub Copilot Instructions - Python Backend Pro Max

## Skill Overview
This project uses the **Python Backend Pro Max** skill for Python backend development best practices.

### Skill Location
- Main skill file: `.shared/SKILL.md`
- Reference documents: `.shared/references/`
- Knowledge database: `.shared/data/`
- Search scripts: `.shared/scripts/`

### Reference Documents
- `.shared/references/fastapi.md` - FastAPI best practices
- `.shared/references/security.md` - Security patterns
- `.shared/references/database.md` - Database operations
- `.shared/references/upstash.md` - Redis/Upstash integration
- `.shared/references/deslop.md` - Code cleanup guidelines
- `.shared/references/api.md` - API design patterns
- `.shared/references/perf.md` - Performance optimization
- `.shared/references/template.md` - Project templates

### Search Commands
```bash
python3 .shared/scripts/search.py "query" --domain fastapi
python3 .shared/scripts/knowledge_db.py "query"
```

## When to Use
- Building FastAPI REST APIs
- Implementing authentication (JWT, OAuth2)
- Working with SQLAlchemy databases
- Setting up Redis caching
- Refactoring AI-generated code
- Optimizing performance

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
