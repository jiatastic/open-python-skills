# Windsurf Rules - open-python-skills

## Skill Location
The open-python-skills skill is located at `.shared/SKILL.md`.

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

### Search Scripts
```bash
# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"

# Get full entry
python3 .shared/scripts/knowledge_db.py --get entry-id

# List categories / tags
python3 .shared/scripts/knowledge_db.py --list-categories
python3 .shared/scripts/knowledge_db.py --list-tags

# Stats
python3 .shared/scripts/knowledge_db.py --stats
```

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
