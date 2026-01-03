#!/usr/bin/env python3
"""
Open Python Skills CLI - Install skill to different AI assistants

Usage:
    open-python-skills init --cursor      # Install to Cursor
    open-python-skills init --claude      # Install to Claude Code
    open-python-skills init --windsurf    # Install to Windsurf
    open-python-skills init --kiro        # Install to Kiro
    open-python-skills init --copilot     # Install to GitHub Copilot
    open-python-skills init --antigravity # Install to Antigravity (.agent + .shared)
    open-python-skills init --all         # Install to all assistants
"""

import argparse
import json
import os
import sys
from pathlib import Path


SKILL_NAME = "open-python-skills"
SKILL_PATH = ".shared/SKILL.md"
SKILL_DESCRIPTION = "Python backend development expertise for FastAPI, security, database, caching"


def get_project_root() -> Path:
    """Get project root directory from environment or current directory."""
    # Check environment variable first
    if project_root := os.environ.get("OPEN_PYTHON_SKILLS_PROJECT"):
        return Path(project_root).expanduser().resolve()
    
    # Try to find .shared in current directory or parents
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / ".shared" / "SKILL.md").exists():
            return path
    
    # Default to current directory
    return current


def check_shared_exists() -> bool:
    """Check if .shared directory exists."""
    project_root = get_project_root()
    shared_path = project_root / ".shared"
    skill_file = project_root / SKILL_PATH
    
    if not shared_path.exists():
        print(f"❌ Error: {shared_path} directory not found!")
        print(f"   Please ensure the skill is located at {skill_file}")
        print(f"\n💡 Solutions:")
        print(f"   1. Run from project root directory")
        print(f"   2. Set environment variable: export OPEN_PYTHON_SKILLS_PROJECT=/path/to/project")
        print(f"   3. Clone the project: git clone <repo-url>")
        return False
    
    if not skill_file.exists():
        print(f"❌ Error: {skill_file} not found!")
        return False
    
    return True


def install_cursor(base_path: Path) -> bool:
    """Install skill to Cursor IDE."""
    cursor_dir = base_path / ".cursor" / "commands"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    command_file = cursor_dir / f"{SKILL_NAME}.md"
    
    content = """# Python Backend Pro Max

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
"""
    
    command_file.write_text(content, encoding="utf-8")
    print(f"✅ Installed to Cursor: {command_file}")
    return True


def install_claude(base_path: Path) -> bool:
    """Install skill to Claude Code."""
    claude_dir = base_path / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    
    # Update settings.local.json
    settings_file = claude_dir / "settings.local.json"
    
    settings = {
        "skills": [
            {
                "name": SKILL_NAME,
                "path": SKILL_PATH,
                "description": SKILL_DESCRIPTION
            }
        ],
        "commands": {
            "search-fastapi": {
                "description": "Search FastAPI best practices",
                "command": "python3 .shared/scripts/search.py \"$QUERY\" --domain fastapi"
            },
            "search-security": {
                "description": "Search security patterns",
                "command": "python3 .shared/scripts/search.py \"$QUERY\" --domain security"
            },
            "search-db": {
                "description": "Search knowledge database",
                "command": "python3 .shared/scripts/knowledge_db.py \"$QUERY\""
            }
        }
    }
    
    settings_file.write_text(json.dumps(settings, indent=2), encoding="utf-8")
    
    # Update commands.md
    commands_file = claude_dir / "commands.md"
    commands_content = """# Claude Code Commands

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
"""
    
    commands_file.write_text(commands_content, encoding="utf-8")
    print(f"✅ Installed to Claude Code: {settings_file}, {commands_file}")
    return True


def install_windsurf(base_path: Path) -> bool:
    """Install skill to Windsurf IDE."""
    windsurf_dir = base_path / ".windsurf"
    windsurf_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = windsurf_dir / "rules.md"
    
    content = f"""# Windsurf Rules - Python Backend Pro Max

## Skill Location
The Python Backend Pro Max skill is located at `{SKILL_PATH}`.

## When to Activate
Activate this skill when working with:
- Python backend development
- FastAPI applications
- REST API design
- Authentication/authorization
- Database operations with SQLAlchemy
- Redis/caching integration
- Performance optimization

## Available Resources

### Reference Documents
Read these markdown files for patterns and examples:
- `.shared/references/fastapi.md` - FastAPI best practices
- `.shared/references/security.md` - Security patterns
- `.shared/references/database.md` - Database operations
- `.shared/references/upstash.md` - Redis/Upstash integration
- `.shared/references/deslop.md` - Code cleanup guidelines
- `.shared/references/api.md` - API design patterns
- `.shared/references/perf.md` - Performance optimization
- `.shared/references/template.md` - Project templates

### Search Scripts
```bash
# Search reference documents
python3 .shared/scripts/search.py "query" --domain fastapi

# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"

# Get full entry
python3 .shared/scripts/knowledge_db.py --get entry-id
```

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
"""
    
    rules_file.write_text(content, encoding="utf-8")
    print(f"✅ Installed to Windsurf: {rules_file}")
    return True


def install_kiro(base_path: Path) -> bool:
    """Install skill to Kiro IDE."""
    kiro_dir = base_path / ".kiro"
    kiro_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = kiro_dir / "rules.md"
    
    content = f"""# Kiro Rules - Python Backend Pro Max

## Skill
This project includes the **Python Backend Pro Max** skill for Python backend development.

### Skill Entry Point
`{SKILL_PATH}`

### Knowledge Sources
1. **Reference Documents** (`.shared/references/*.md`)
   - 8 comprehensive guides covering FastAPI, security, database, etc.

2. **Knowledge Database** (`.shared/data/*.json`)
   - 22 curated best practices from zhanymkanov/fastapi-best-practices

### Search Commands
```bash
# Reference search
python3 .shared/scripts/search.py "jwt" --domain security

# Knowledge database search
python3 .shared/scripts/knowledge_db.py "async routes"
python3 .shared/scripts/knowledge_db.py --get async-routes-io
python3 .shared/scripts/knowledge_db.py --list-categories
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
"""
    
    rules_file.write_text(content, encoding="utf-8")
    print(f"✅ Installed to Kiro: {rules_file}")
    return True


def install_copilot(base_path: Path) -> bool:
    """Install skill to GitHub Copilot."""
    copilot_dir = base_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True, exist_ok=True)
    
    instructions_file = copilot_dir / "instructions.md"
    
    content = f"""# GitHub Copilot Instructions - Python Backend Pro Max

## Skill Overview
This project uses the **Python Backend Pro Max** skill for Python backend development best practices.

### Skill Location
- Main skill file: `{SKILL_PATH}`
- Reference documents: `.shared/references/`
- Knowledge database: `.shared/data/`
- Search scripts: `.shared/scripts/`

### Reference Documents
- `.shared/references/fastapi.md` - FastAPI best practices
- `.shared/references/security.md` - Security patterns
- `.shared/references/database.md` - Database operations
- `.shared/references/upstash.md` - Redis/Upstash integration
- `.shared/references/deslop.md` - Code cleanup guidelines
- `.shared/references/api.md` - API design patterns
- `.shared/references/perf.md` - Performance optimization
- `.shared/references/template.md` - Project templates

### Search Commands
```bash
python3 .shared/scripts/search.py "query" --domain fastapi
python3 .shared/scripts/knowledge_db.py "query"
```

## When to Use
- Building FastAPI REST APIs
- Implementing authentication (JWT, OAuth2)
- Working with SQLAlchemy databases
- Setting up Redis caching
- Refactoring AI-generated code
- Optimizing performance

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validation
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
"""
    
    instructions_file.write_text(content, encoding="utf-8")
    print(f"✅ Installed to GitHub Copilot: {instructions_file}")
    return True


def install_antigravity(base_path: Path) -> bool:
    """Install skill to Antigravity (.agent + .shared)."""
    agent_dir = base_path / ".agent"
    agent_dir.mkdir(parents=True, exist_ok=True)
    
    agents_file = agent_dir / "AGENTS.md"
    
    content = f"""# OpenSkills Universal Configuration

## Skill: {SKILL_NAME}

### Entry Point
`{SKILL_PATH}`

### Description
{SKILL_DESCRIPTION}

### Knowledge Sources
- Reference Documents: `.shared/references/*.md`
- Knowledge Database: `.shared/data/*.json`
- Search Scripts: `.shared/scripts/*.py`

### Usage
```bash
# Search reference documents
python3 .shared/scripts/search.py "query" --domain fastapi

# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"
python3 .shared/scripts/knowledge_db.py --get entry-id
```

### Supported IDEs
- Cursor
- Claude Code
- Windsurf
- Kiro
- GitHub Copilot
- Antigravity
"""
    
    agents_file.write_text(content, encoding="utf-8")
    print(f"✅ Installed to Antigravity: {agents_file}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Install open-python-skills to AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    init_parser = subparsers.add_parser("init", help="Initialize skill installation")
    init_parser.add_argument("--cursor", action="store_true", help="Install to Cursor")
    init_parser.add_argument("--claude", action="store_true", help="Install to Claude Code")
    init_parser.add_argument("--windsurf", action="store_true", help="Install to Windsurf")
    init_parser.add_argument("--kiro", action="store_true", help="Install to Kiro")
    init_parser.add_argument("--copilot", action="store_true", help="Install to GitHub Copilot")
    init_parser.add_argument("--antigravity", action="store_true", help="Install to Antigravity")
    init_parser.add_argument("--all", action="store_true", help="Install to all assistants")
    
    args = parser.parse_args()
    
    if args.command != "init":
        parser.print_help()
        sys.exit(1)
    
    # Check if .shared exists
    if not check_shared_exists():
        sys.exit(1)
    
    base_path = get_project_root()
    success_count = 0
    total_count = 0
    
    installers = []
    
    if args.all:
        installers = [
            ("Cursor", install_cursor),
            ("Claude Code", install_claude),
            ("Windsurf", install_windsurf),
            ("Kiro", install_kiro),
            ("GitHub Copilot", install_copilot),
            ("Antigravity", install_antigravity),
        ]
    else:
        if args.cursor:
            installers.append(("Cursor", install_cursor))
        if args.claude:
            installers.append(("Claude Code", install_claude))
        if args.windsurf:
            installers.append(("Windsurf", install_windsurf))
        if args.kiro:
            installers.append(("Kiro", install_kiro))
        if args.copilot:
            installers.append(("GitHub Copilot", install_copilot))
        if args.antigravity:
            installers.append(("Antigravity", install_antigravity))
    
    if not installers:
        print("❌ Error: No IDE specified!")
        print("   Use --cursor, --claude, --windsurf, --kiro, --copilot, --antigravity, or --all")
        sys.exit(1)
    
    print(f"\n🚀 Installing {SKILL_NAME} to {len(installers)} IDE(s)...\n")
    
    for name, installer_func in installers:
        total_count += 1
        try:
            if installer_func(base_path):
                success_count += 1
        except Exception as e:
            print(f"❌ Failed to install to {name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"✅ Successfully installed to {success_count}/{total_count} IDE(s)")
    print(f"{'='*60}\n")


def main_entry():
    """Entry point for console script."""
    main()


if __name__ == "__main__":
    main()
