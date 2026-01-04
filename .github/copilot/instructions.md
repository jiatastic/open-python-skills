# GitHub Copilot Instructions - open-python-skills

## Skill Overview
This project uses the **open-python-skills** knowledge base for Python backend development best practices.

### Skill Location
- Main skill file: `.shared/SKILL.md`
- Knowledge database: `.shared/data/`
- Search scripts: `.shared/scripts/`

### Search Commands
```bash
python3 .shared/scripts/knowledge_db.py "query"
python3 .shared/scripts/knowledge_db.py "query" --category security
python3 .shared/scripts/knowledge_db.py --get entry-id
python3 .shared/scripts/knowledge_db.py --list-categories
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
