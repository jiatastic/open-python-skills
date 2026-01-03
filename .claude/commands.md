# Claude Code Commands

## Python Backend Pro Max Skill

### Available Commands

#### Search Reference Documents
```bash
# Search all domains
python3 .shared/scripts/search.py "jwt authentication"

# Search specific domain
python3 .shared/scripts/search.py "dependency injection" --domain fastapi
python3 .shared/scripts/search.py "password hashing" --domain security
python3 .shared/scripts/search.py "connection pooling" --domain database
```

#### Search Knowledge Database
```bash
# Search curated best practices
python3 .shared/scripts/knowledge_db.py "async routes"

# Filter by category
python3 .shared/scripts/knowledge_db.py "validation" --category pydantic

# Get full entry with code
python3 .shared/scripts/knowledge_db.py --get async-routes-io

# List all categories
python3 .shared/scripts/knowledge_db.py --list-categories
```

### Domain Reference Quick Links

| Domain | Path | Topics |
|--------|------|--------|
| FastAPI | `.shared/references/fastapi.md` | Project structure, DI, async |
| Security | `.shared/references/security.md` | JWT, OAuth2, CORS |
| Database | `.shared/references/database.md` | SQLAlchemy 2.0, migrations |
| Upstash | `.shared/references/upstash.md` | Redis, QStash |
| Deslop | `.shared/references/deslop.md` | AI code cleanup |
| API | `.shared/references/api.md` | REST patterns |
| Perf | `.shared/references/perf.md` | Optimization |
| Template | `.shared/references/template.md` | Project templates |
