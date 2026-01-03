# Claude Code Commands

## Python Backend Pro Max Skill

### Available Commands

#### Search Reference Documents
```bash
# Search all domains
python3 .shared/open-python-skills/scripts/search.py "jwt authentication"

# Search specific domain
python3 .shared/open-python-skills/scripts/search.py "dependency injection" --domain fastapi
python3 .shared/open-python-skills/scripts/search.py "password hashing" --domain security
python3 .shared/open-python-skills/scripts/search.py "connection pooling" --domain database
```

#### Search Knowledge Database
```bash
# Search curated best practices
python3 .shared/open-python-skills/scripts/knowledge_db.py "async routes"

# Filter by category
python3 .shared/open-python-skills/scripts/knowledge_db.py "validation" --category pydantic

# Get full entry with code
python3 .shared/open-python-skills/scripts/knowledge_db.py --get async-routes-io

# List all categories
python3 .shared/open-python-skills/scripts/knowledge_db.py --list-categories
```

### Domain Reference Quick Links

| Domain | Path | Topics |
|--------|------|--------|
| FastAPI | `.shared/open-python-skills/references/fastapi.md` | Project structure, DI, async |
| Security | `.shared/open-python-skills/references/security.md` | JWT, OAuth2, CORS |
| Database | `.shared/open-python-skills/references/database.md` | SQLAlchemy 2.0, migrations |
| Upstash | `.shared/open-python-skills/references/upstash.md` | Redis, QStash |
| Deslop | `.shared/open-python-skills/references/deslop.md` | AI code cleanup |
| API | `.shared/open-python-skills/references/api.md` | REST patterns |
| Perf | `.shared/open-python-skills/references/perf.md` | Optimization |
| Template | `.shared/open-python-skills/references/template.md` | Project templates |
