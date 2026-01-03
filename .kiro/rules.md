# Kiro Rules - Python Backend Pro Max

## Skill
This project includes the **Python Backend Pro Max** skill for Python backend development.

### Skill Entry Point
`.shared/open-python-skills/SKILL.md`

### Knowledge Sources
1. **Reference Documents** (`.shared/open-python-skills/references/*.md`)
   - 8 comprehensive guides covering FastAPI, security, database, etc.

2. **Knowledge Database** (`.shared/open-python-skills/data/*.json`)
   - 21 curated best practices from zhanymkanov/fastapi-best-practices

### Search Commands
```bash
# Reference search
python3 .shared/open-python-skills/scripts/search.py "jwt" --domain security

# Knowledge database search
python3 .shared/open-python-skills/scripts/knowledge_db.py "async routes"
python3 .shared/open-python-skills/scripts/knowledge_db.py --get async-routes-io
python3 .shared/open-python-skills/scripts/knowledge_db.py --list-categories
```

## Activation Triggers
Use this skill when:
- Building FastAPI REST APIs
- Implementing authentication (JWT, OAuth2)
- Working with SQLAlchemy databases
- Setting up Redis caching
- Refactoring AI-generated code
- Optimizing performance

## Principles
- Async-first for I/O
- Pydantic for validation
- Dependency injection
- Fail fast
- Security by default
