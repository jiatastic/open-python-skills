# Open Python Skills

CLI tool to install AI coding skills to your projects. Currently includes:
- **python-backend** - FastAPI, SQLAlchemy, Redis, security patterns
- **commit-message** - Git commit message analysis and batch commit suggestions
- **excalidraw-ai** - AI-powered Excalidraw diagram generator from text descriptions
- **ty-skills** - Python type checking with ty (Astral's type checker)

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
| `excalidraw-ai` | Generate Excalidraw diagrams from natural language descriptions |
| `ty-skills` | Python type checking with ty, migration guides, typing patterns |

## What It Does

Running `init` copies skill files to your project. All IDEs use the same `.shared/` directory for consistent skill content:

```
your-project/
├── .shared/                      # Skills (same for all IDEs)
│   ├── python-backend/
│   │   ├── SKILL.md
│   │   ├── data/*.json
│   │   └── scripts/
│   ├── commit-message/
│   ├── excalidraw-ai/
│   └── ty-skills/
├── .cursor/commands/             # (if --cursor)
├── .claude/                      # (if --claude)
│   ├── CLAUDE.md
│   └── commands/
├── .windsurf/rules.md            # (if --windsurf)
├── .kiro/rules.md                # (if --kiro)
└── .github/copilot/instructions.md  # (if --copilot)
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

### excalidraw-ai

Generate Excalidraw diagrams from natural language descriptions.

```bash
# Generate flowchart
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "User Login -> Auth -> Access Data" --type flowchart

# Generate architecture diagram
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "API Gateway -> Microservice -> Database" --type architecture

# Generate backend architecture from a Python project (context-aware)
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --output backend_arch.json
```

**Types:** `flowchart`, `architecture`, `mindmap`

### ty-skills

Python type checking guidance with ty (Astral's ultra-fast type checker).

**References included:**
- `typing_cheatsheet.md` - Quick reference for Python typing
- `ty_rules_reference.md` - All ty error codes and fixes
- `migration_guide.md` - Migrating from mypy/pyright to ty
- `advanced_patterns.md` - Complex typing patterns
- `common_errors.md` - Common errors and solutions
- `editor_setup/` - Setup guides for VSCode, Cursor, Neovim

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
