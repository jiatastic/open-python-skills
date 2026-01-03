# Windsurf Rules - Python Backend Pro Max

## Skill Location
The Python Backend Pro Max skill is located at `.shared/SKILL.md`.

## When to Activate
Activate this skill when working with:
- Python backend development
- FastAPI applications
- REST API design
- Authentication/authorization
- Database operations with SQLAlchemy
- Redis/caching integration
- Performance optimization

## Available Resources

### Reference Documents
Read these markdown files for patterns and examples:
- `.shared/references/fastapi.md` - FastAPI best practices
- `.shared/references/security.md` - Security patterns
- `.shared/references/database.md` - Database operations
- `.shared/references/upstash.md` - Redis/Upstash integration
- `.shared/references/deslop.md` - Code cleanup guidelines
- `.shared/references/api.md` - API design patterns
- `.shared/references/perf.md` - Performance optimization
- `.shared/references/template.md` - Project templates

### Search Scripts
```bash
# Search reference documents
python3 .shared/scripts/search.py "query" --domain fastapi

# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"

# Get full entry
python3 .shared/scripts/knowledge_db.py --get entry-id
```

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
