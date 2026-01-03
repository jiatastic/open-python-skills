# Python Backend Pro Max

Search and use Python backend best practices from the knowledge base.

## Instructions

1. Search reference documents:
   ```bash
   python3 .shared/scripts/search.py "{{query}}" --domain {{domain}}
   ```

2. Search knowledge database:
   ```bash
   python3 .shared/scripts/knowledge_db.py "{{query}}"
   ```

3. Get full entry with code examples:
   ```bash
   python3 .shared/scripts/knowledge_db.py --get {{entry-id}}
   ```

## Available Domains

- `fastapi` - Project structure, DI, async patterns, Pydantic
- `security` - JWT, OAuth2, password hashing, API keys, CORS
- `database` - SQLAlchemy 2.0, async operations, migrations
- `upstash` - Redis caching, QStash background jobs
- `deslop` - AI code cleanup, refactoring patterns
- `api` - REST patterns, versioning, pagination
- `perf` - Caching, profiling, optimization
- `template` - Project templates, architectures

## Reference Documents

Located in `.shared/references/`:
- fastapi.md, security.md, database.md, upstash.md
- deslop.md, api.md, perf.md, template.md

## Knowledge Database

- `.shared/data/fastapi_best_practices.json` - 22 curated entries

## Examples

- `/open-python-skills async routes`
- `/open-python-skills jwt authentication`
- `/open-python-skills pydantic validation`
- `/open-python-skills database connection pooling`
