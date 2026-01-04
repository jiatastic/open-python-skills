# Open Python Skills

CLI tool to install AI coding skills to your projects. Currently includes **python-backend** skill for FastAPI, SQLAlchemy, Redis, security patterns.

## Quick Start

```bash
# Install skill to your project (no pip install needed)
uvx open-python-skills init --cursor      # Cursor
uvx open-python-skills init --claude      # Claude Code
uvx open-python-skills init --windsurf    # Windsurf
uvx open-python-skills init --all         # All IDE
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `python-backend` | FastAPI, SQLAlchemy, Redis, security, performance patterns |

## What It Does

Running `init` copies skill files to your project:

```
your-project/
├── .shared/
│   ├── SKILL.md              # Skill description for AI
│   ├── data/                 # Knowledge databases
│   │   └── *.json
│   └── scripts/
│       └── knowledge_db.py   # Search script
├── .cursor/commands/         # (if --cursor)
└── ...
```

Your AI assistant can then search the knowledge base for patterns and best practices.

## Categories (python-backend)

| Category | Description |
|----------|-------------|
| `fastapi` | Project structure, async patterns, Pydantic |
| `security` | JWT/OAuth2, password hashing, CORS |
| `database` | SQLAlchemy, Alembic, connection pooling |
| `upstash` | Redis caching, QStash jobs, rate limiting |
| `performance` | Caching, async, profiling |
| `api` | REST conventions, versioning |
| `deslop` | AI code cleanup patterns |

## Requirements

- Python 3.8+

## License

MIT
