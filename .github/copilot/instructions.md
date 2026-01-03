# GitHub Copilot Instructions

## Python Backend Pro Max Skill

This repository includes a Python backend development skill with comprehensive documentation.

### Skill Location
- Main skill file: `.shared/open-python-skills/SKILL.md`
- Reference documents: `.shared/open-python-skills/references/`
- Knowledge database: `.shared/open-python-skills/data/`
- Search scripts: `.shared/open-python-skills/scripts/`

### Reference Documents

| File | Topics |
|------|--------|
| `fastapi.md` | Project structure, dependency injection, async patterns, Pydantic |
| `security.md` | JWT, OAuth2, password hashing, API keys, CORS, rate limiting |
| `database.md` | SQLAlchemy 2.0, async operations, migrations, connection pooling |
| `upstash.md` | Redis caching, session management, QStash background jobs |
| `deslop.md` | AI code cleanup, refactoring patterns, naming conventions |
| `api.md` | RESTful principles, versioning, pagination, error handling |
| `perf.md` | Caching strategies, async optimization, profiling |
| `template.md` | Project templates, microservice architecture |

### Search Commands
```bash
python3 .shared/open-python-skills/scripts/search.py "query" --domain fastapi
python3 .shared/open-python-skills/scripts/knowledge_db.py "query"
```

### Best Practices
1. Use async/await for I/O operations
2. Validate with Pydantic models
3. Use FastAPI's Depends() for dependency injection
4. Validate early, fail fast with HTTPException
5. Never trust user input, always hash passwords
