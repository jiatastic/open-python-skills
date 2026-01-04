# Kiro Rules - open-python-skills

## Skill
This project includes the **open-python-skills** knowledge base for Python backend development.

### Skill Entry Point
`.shared/SKILL.md`

### Knowledge Sources
1. **Knowledge Database** (`.shared/data/*.json`)
   - Incremental, searchable best practices and patterns (FastAPI, security, database, upstash, etc.)

### Search Commands
```bash
# Knowledge database search
python3 .shared/scripts/knowledge_db.py "async routes"
python3 .shared/scripts/knowledge_db.py --get async-routes-io
python3 .shared/scripts/knowledge_db.py --list-categories
python3 .shared/scripts/knowledge_db.py --list-tags
python3 .shared/scripts/knowledge_db.py --stats
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
