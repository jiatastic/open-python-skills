# Windsurf Rules - Python Backend Pro Max

## Skill Location
The Python Backend Pro Max skill is located at `.shared/open-python-skills/SKILL.md`.

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
- `.shared/open-python-skills/references/fastapi.md` - FastAPI best practices
- `.shared/open-python-skills/references/security.md` - Security patterns
- `.shared/open-python-skills/references/database.md` - Database operations
- `.shared/open-python-skills/references/upstash.md` - Redis/Upstash integration
- `.shared/open-python-skills/references/deslop.md` - Code cleanup guidelines
- `.shared/open-python-skills/references/api.md` - API design patterns
- `.shared/open-python-skills/references/perf.md` - Performance optimization
- `.shared/open-python-skills/references/template.md` - Project templates

### Search Scripts
```bash
# Search reference documents
python3 .shared/open-python-skills/scripts/search.py "query" --domain fastapi

# Search knowledge database
python3 .shared/open-python-skills/scripts/knowledge_db.py "query"

# Get full entry
python3 .shared/open-python-skills/scripts/knowledge_db.py --get entry-id
```

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
