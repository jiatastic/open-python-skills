# Open Python Skills

> 🧠 Supercharge your AI code editor with Python development skills

One command to make Cursor / Claude Code / Windsurf / Kiro / Copilot understand FastAPI best practices, commit conventions, architecture diagrams, and type checking.

## Why Use This?

| Scenario | Before 😅 | After ✨ |
|----------|-----------|----------|
| Writing commits | `fix stuff` | `feat(auth): add JWT refresh token rotation` |
| Drawing architecture | Spend 2 hours in draw.io | Describe it, AI generates Excalidraw |
| Asking FastAPI questions | AI gives outdated answers | AI searches local knowledge base |
| Type checking | `# type: ignore` everywhere | ty handles it, zero errors |

## Quick Start

```bash
# No pip install needed, just run with uvx
uvx open-python-skills init --cursor      # Cursor
uvx open-python-skills init --claude      # Claude Code
uvx open-python-skills init --windsurf    # Windsurf
uvx open-python-skills init --kiro        # Kiro
uvx open-python-skills init --copilot     # GitHub Copilot
uvx open-python-skills init --all         # All of them!
```

## Available Skills

| Skill | What It Does |
|-------|--------------|
| `python-backend` | FastAPI + SQLAlchemy + Redis + Security patterns |
| `commit-message` | Analyze git changes, generate conventional commits |
| `excalidraw-ai` | Generate diagrams from natural language |
| `ty-skills` | Complete guide for Astral's ty type checker |

---

## Skill Details

<details>
<summary><b>🔧 python-backend</b> — Python Backend Knowledge Base</summary>

### Includes
- 🚀 FastAPI best practices
- 🔐 Security patterns (JWT, CORS, Rate Limiting)
- 🗄️ SQLAlchemy database patterns
- ⚡ Redis / Upstash caching strategies
- 📊 Performance optimization tips

### Usage

```bash
# Search knowledge base
python3 .shared/python-backend/scripts/knowledge_db.py "jwt authentication"

# Filter by category
python3 .shared/python-backend/scripts/knowledge_db.py "caching" --category upstash
```

**Categories:** `fastapi` `security` `database` `upstash` `performance` `api` `template`

</details>

<details>
<summary><b>📝 commit-message</b> — Smart Git Commit Generator</summary>

### Features
- ✅ Conventional Commits format (`feat`, `fix`, `refactor`, etc.)
- ✅ Auto-grouping by directory/module
- ✅ Batch commit suggestions for large changesets

### Usage

```bash
# Analyze all changes
python3 .shared/commit-message/scripts/analyze_changes.py --analyze

# Get batch commit suggestions
python3 .shared/commit-message/scripts/analyze_changes.py --batch

# Generate message for specific files
python3 .shared/commit-message/scripts/analyze_changes.py --generate "src/*.py"
```

</details>

<details>
<summary><b>🎨 excalidraw-ai</b> — AI Diagram Generator</summary>

### Features
- ✅ Natural language → Excalidraw JSON
- ✅ Supports flowcharts, architecture diagrams, mindmaps
- ✅ Can analyze project code to auto-generate architecture

### Usage

```bash
# Generate flowchart
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "User Login -> Auth -> Access Data" --type flowchart

# Generate architecture diagram
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "API Gateway -> Microservice -> Database" --type architecture

# Analyze project and generate architecture
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --output arch.json
```

**Types:** `flowchart` `architecture` `mindmap`

</details>

<details>
<summary><b>🔍 ty-skills</b> — Python Type Checking Guide</summary>

### Includes
- 📖 `typing_cheatsheet.md` — Quick reference for Python typing
- 📖 `ty_rules_reference.md` — All ty error codes and fixes
- 📖 `migration_guide.md` — Migrating from mypy/pyright
- 📖 `advanced_patterns.md` — Advanced typing patterns
- 📖 `common_errors.md` — Common errors and solutions
- 📖 `editor_setup/` — VSCode / Cursor / Neovim setup guides

</details>

---

## Project Structure After Install

```
your-project/
├── .shared/                      # Skills (shared across all IDEs)
│   ├── python-backend/
│   ├── commit-message/
│   ├── excalidraw-ai/
│   └── ty-skills/
├── .cursor/commands/             # Cursor commands
├── .claude/                      # Claude Code config
├── .windsurf/rules.md            # Windsurf rules
├── .kiro/rules.md                # Kiro rules
└── .github/copilot/instructions.md  # Copilot instructions
```

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
