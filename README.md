# Open Python Skills

> 🧠 Supercharge your AI code editor with Python development skills

One command makes Cursor / Claude Code / Windsurf / Kiro / Copilot understand FastAPI best practices, commit conventions, architecture diagrams, and Python type checking.

## Why This Exists

- **Faster answers**: local knowledge beats generic internet snippets.
- **Better commits**: structured Conventional Commits without guesswork.
- **Instant diagrams**: describe architecture, get Excalidraw JSON.
- **Type safety**: practical guides for Astral's `ty` type checker.

## Quick Start (Recommended)

```bash
# No pip install needed, just run with uvx
uvx open-python-skills init --cursor      # Cursor
uvx open-python-skills init --claude      # Claude Code
uvx open-python-skills init --windsurf    # Windsurf
uvx open-python-skills init --kiro        # Kiro
uvx open-python-skills init --copilot     # GitHub Copilot
uvx open-python-skills init --all         # All of them!
```

## Install Options

```bash
# Install globally
pip install open-python-skills

# Then initialize in your project
open-python-skills init --cursor
```

## Available Skills

| Skill | What It Does |
|-------|--------------|
| `python-backend` | FastAPI + SQLAlchemy + Redis + security patterns |
| `commit-message` | Analyze git changes, generate Conventional Commits |
| `excalidraw-ai` | Generate Excalidraw diagrams from text |
| `ty-skills` | Complete guide for Astral's ty type checker |
| `unit-testing` | Practical pytest patterns, fixtures, and mocks |
| `docker-builder` | Production Dockerfiles and compose patterns |
| `web-scraping` | Requests/BeautifulSoup/Playwright scraping patterns |
| `api-testing` | OpenAPI-driven testing with schemathesis |
| `linting` | Ruff linting rules and workflows |
| `formatting` | Black/Ruff-format conventions |
| `observability` | OpenTelemetry + Logfire for APIs |
| `error-handling` | API error schemas and handling patterns |
| `marimo-notebook` | Reproducible marimo notebooks |
| `pydantic` | Pydantic models and validation |

## Common Commands

```bash
open-python-skills init [--cursor|--claude|--windsurf|--kiro|--copilot|--all]
open-python-skills search "query"
open-python-skills get <entry-id>
open-python-skills categories
open-python-skills stats
```

## Example Usage

```bash
# Search FastAPI patterns
open-python-skills search "jwt authentication"

# Get a specific entry
open-python-skills get fastapi-013

# List categories
open-python-skills categories

# Generate batch commit suggestions
python3 .shared/commit-message/scripts/analyze_changes.py --batch

# Generate an architecture diagram
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "API Gateway -> Service -> DB" --type architecture
```

## How It Works

1. The package ships bundled skills inside `open_python_skills/`.
2. `open-python-skills init ...` copies them into `.shared/` in your project.
3. It also writes IDE-specific command/rule files (Cursor, Claude, Windsurf, Kiro, Copilot).

## Skill Details

<details>
<summary><b>🔧 python-backend</b> — Python Backend Knowledge Base</summary>

### Includes
- 🚀 FastAPI best practices
- 🔐 Security patterns (JWT, CORS, rate limiting)
- 🗄️ SQLAlchemy database patterns
- ⚡ Redis / Upstash caching strategies
- 📊 Performance optimization tips

### Usage

```bash
python3 .shared/python-backend/scripts/knowledge_db.py "jwt authentication"
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
python3 .shared/commit-message/scripts/analyze_changes.py --analyze
python3 .shared/commit-message/scripts/analyze_changes.py --batch
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
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "User Login -> Auth -> Access Data" --type flowchart
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "API Gateway -> Microservice -> Database" --type architecture
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

## FAQ

**Where is the knowledge stored?**
All skill data lives in `.shared/<skill>/` after installation.

**How do I update the skills?**
Re-run `open-python-skills init --all` in your project.

**Can I install to just one IDE?**
Yes—use a single flag like `--cursor` or `--claude`.

## Requirements

- Python 3.8+

## License

MIT
