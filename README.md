# Open Python Skills

CLI tool to install AI coding skills to your projects. Currently includes:
- **python-backend** - FastAPI, SQLAlchemy, Redis, security patterns
- **commit-message** - Git commit message analysis and batch commit suggestions

## Quick Start

```bash
# Install all skills to your project (no pip install needed)
uvx open-python-skills init --cursor      # Cursor
uvx open-python-skills init --claude      # Claude Code
uvx open-python-skills init --windsurf    # Windsurf
uvx open-python-skills init --kiro        # Kiro
uvx open-python-skills init --copilot     # GitHub Copilot
uvx open-python-skills init --all         # All IDEs
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `python-backend` | FastAPI, SQLAlchemy, Redis, security, performance patterns |
| `commit-message` | Analyze git changes and generate conventional commit messages |

## What It Does

Running `init` copies skill files to your project:

```
your-project/
├── .shared/
│   ├── python-backend/
│   │   ├── SKILL.md
│   │   ├── data/*.json
│   │   └── scripts/knowledge_db.py
│   └── commit-message/
│       ├── SKILL.md
│       ├── data/*.json
│       └── scripts/analyze_changes.py
├── .cursor/commands/     # (if --cursor)
│   ├── kb-search.md
│   └── commit-batch.md
└── ...
```

## Skills Overview

### python-backend

Searchable knowledge base for Python backend development.

```bash
# Search knowledge database
python3 .shared/python-backend/scripts/knowledge_db.py "jwt authentication"

# Filter by category
python3 .shared/python-backend/scripts/knowledge_db.py "caching" --category upstash
```

**Categories:** `fastapi`, `security`, `database`, `upstash`, `performance`, `api`, `deslop`, `template`

### commit-message

Analyze git changes and generate context-aware commit messages.

```bash
# Analyze all changes
python3 .shared/commit-message/scripts/analyze_changes.py --analyze

# Get batch commit suggestions
python3 .shared/commit-message/scripts/analyze_changes.py --batch

# Generate message for specific files
python3 .shared/commit-message/scripts/analyze_changes.py --generate "src/*.py"
```

**Features:**
- Conventional commit format (`feat`, `fix`, `refactor`, `docs`, etc.)
- Automatic grouping by directory/module
- Batch commit suggestions for large changesets

## CLI Commands

```bash
open-python-skills init [--cursor|--claude|--windsurf|--all]  # Install skills
open-python-skills search "query"                              # Search knowledge
open-python-skills get <entry-id>                              # Get full entry
open-python-skills categories                                  # List categories
open-python-skills stats                                       # Show statistics
```

## Requirements

- Python 3.8+

## License

MIT
