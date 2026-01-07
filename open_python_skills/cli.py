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
    
    open-python-skills search "query"     # Search knowledge database
    open-python-skills get <entry-id>     # Get full entry
    open-python-skills categories         # List all categories
    open-python-skills stats              # Show statistics
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

try:
    from importlib.resources import files as importlib_files
except ImportError:
    # Python 3.8 fallback. This optional dependency is only needed on 3.8.
    from importlib_resources import files as importlib_files  # type: ignore[import-not-found]


SKILL_NAME = "open-python-skills"
SKILL_PATH = ".shared/SKILL.md"
SKILL_DESCRIPTION = "Python backend development expertise for FastAPI, security, database, caching, and best practices"


AVAILABLE_SKILLS = ["python-backend", "commit-message", "excalidraw-ai", "ty-skills"]


def get_package_skill_path(skill_name: str = "python-backend") -> Path:
    """Get path to bundled skill files in package."""
    try:
        return Path(importlib_files("open_python_skills") / skill_name)
    except TypeError:
        # importlib_files may fail if package not properly installed
        return Path(__file__).parent / skill_name


def get_target_path() -> Path:
    """Get target path for installation (current working directory)."""
    return Path.cwd()


def copy_shared_files(target_path: Path, skills: list[str] | None = None) -> bool:
    """Copy .shared files to target project for all skills."""
    if skills is None:
        skills = AVAILABLE_SKILLS

    dest_path = target_path / ".shared"
    dest_path.mkdir(parents=True, exist_ok=True)

    success = True
    for skill_name in skills:
        source_path = get_package_skill_path(skill_name)

        if not source_path.exists():
            print(f"WARNING: Skill '{skill_name}' not found at {source_path}")
            continue

        skill_dest = dest_path / skill_name
        skill_dest.mkdir(parents=True, exist_ok=True)

        # Copy all files from skill
        for item in source_path.iterdir():
            dest_item = skill_dest / item.name
            if item.is_dir():
                if dest_item.exists():
                    shutil.rmtree(dest_item)
                shutil.copytree(item, dest_item)
            else:
                shutil.copy2(item, dest_item)

        print(f"OK: Copied {skill_name} to {skill_dest}")

    return success


def install_cursor(base_path: Path) -> bool:
    """Install skill to Cursor IDE."""
    cursor_dir = base_path / ".cursor" / "commands"
    cursor_dir.mkdir(parents=True, exist_ok=True)
    
    # Main open-python-skills command
    main_command = cursor_dir / "open-python-skills.md"
    main_content = """# open-python-skills

Search and use Python backend best practices from the knowledge base.

## Instructions

1. Search knowledge database:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py "{{query}}"
   ```

2. Filter by category:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py "{{query}}" --category {{category}}
   ```

3. Get full entry with code examples:
   ```bash
   python3 .shared/python-backend/scripts/knowledge_db.py --get {{entry-id}}
   ```

## Available Categories

Use `--list-categories` to discover all categories.

## Knowledge Database

- `.shared/python-backend/data/*.json` (multiple databases; incremental and searchable)

## Examples

- `/open-python-skills async routes`
- `/open-python-skills jwt authentication`
- `/open-python-skills pydantic validation`
- `/open-python-skills database connection pooling`
"""
    main_command.write_text(main_content, encoding="utf-8")
    
    # commit-message skill command
    commit_command = cursor_dir / "commit-batch.md"
    commit_content = """# commit-batch

Analyze git changes and suggest batch commits.

## Instructions

1. Analyze all changes:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --analyze
   ```

2. Get batch commit suggestions:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --batch
   ```

3. Generate message for specific files:
   ```bash
   python3 .shared/commit-message/scripts/analyze_changes.py --generate "*.py"
   ```

## Examples

- `/commit-batch` - Suggest how to split changes into commits
"""
    commit_command.write_text(commit_content, encoding="utf-8")
    
    # excalidraw skill command
    excalidraw_command = cursor_dir / "excalidraw.md"
    excalidraw_content = """# excalidraw

Generate Excalidraw diagram from text.

## Instructions

1. Generate diagram:
   ```bash
   python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "description" --type flowchart
   ```

2. Generate backend architecture from the current Python project:
   ```bash
   python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --output diagram_architecture.json
   ```

## Examples

- `/excalidraw "User login flow" --type flowchart`
- `/excalidraw --project . --type architecture`
"""
    excalidraw_command.write_text(excalidraw_content, encoding="utf-8")
    
    print(f"OK: Installed to Cursor: {cursor_dir}/")
    return True


def install_claude(base_path: Path) -> bool:
    """Install skill to Claude Code."""
    claude_dir = base_path / ".claude"
    commands_dir = claude_dir / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    
    # Create .claude/CLAUDE.md - project memory/instructions
    claude_md = claude_dir / "CLAUDE.md"
    claude_md_content = f"""# {SKILL_NAME}

{SKILL_DESCRIPTION}

## Available Skills

### 1. python-backend
Searchable knowledge base for Python backend development.
See @.shared/python-backend/SKILL.md

```bash
python3 .shared/python-backend/scripts/knowledge_db.py "query"
python3 .shared/python-backend/scripts/knowledge_db.py --get <entry-id>
```

### 2. commit-message
Analyze git changes and generate commit messages.
See @.shared/commit-message/SKILL.md

```bash
python3 .shared/commit-message/scripts/analyze_changes.py --batch
python3 .shared/commit-message/scripts/analyze_changes.py --analyze
```

### 3. excalidraw-ai
Generate diagrams from text.
See @.shared/excalidraw-ai/SKILL.md

```bash
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "description"
```

## Commands

- `/kb-search` - Search python-backend knowledge base
- `/kb-get` - Get full entry by ID
- `/commit-batch` - Suggest batch commits for current changes
- `/commit-analyze` - Analyze git changes
- `/excalidraw` - Generate diagram
"""
    claude_md.write_text(claude_md_content, encoding="utf-8")
    
    # Create .claude/commands/kb-search.md
    kb_search = commands_dir / "kb-search.md"
    kb_search_content = """---
description: Search python-backend knowledge base
argument-hint: [query]
---

Search the knowledge database for: $ARGUMENTS

```bash
python3 .shared/python-backend/scripts/knowledge_db.py "$ARGUMENTS"
```

If results are found, offer to get full details with `/kb-get <entry-id>`.
"""
    kb_search.write_text(kb_search_content, encoding="utf-8")
    
    # Create .claude/commands/kb-get.md
    kb_get = commands_dir / "kb-get.md"
    kb_get_content = """---
description: Get full entry by ID from knowledge base
argument-hint: [entry-id]
---

Get full details for entry: $ARGUMENTS

```bash
python3 .shared/python-backend/scripts/knowledge_db.py --get "$ARGUMENTS"
```
"""
    kb_get.write_text(kb_get_content, encoding="utf-8")
    
    # Create .claude/commands/commit-batch.md
    commit_batch = commands_dir / "commit-batch.md"
    commit_batch_content = """---
description: Suggest batch commits for current changes
---

Analyze git changes and suggest how to split into multiple commits:

```bash
python3 .shared/commit-message/scripts/analyze_changes.py --batch
```

Follow the suggested commit order to create clean, logical commits.
"""
    commit_batch.write_text(commit_batch_content, encoding="utf-8")
    
    # Create .claude/commands/commit-analyze.md
    commit_analyze = commands_dir / "commit-analyze.md"
    commit_analyze_content = """---
description: Analyze git changes
---

Show all changed files with their status:

```bash
python3 .shared/commit-message/scripts/analyze_changes.py --analyze
```
"""
    commit_analyze.write_text(commit_analyze_content, encoding="utf-8")
    
    # Create .claude/commands/excalidraw.md
    excalidraw_cmd = commands_dir / "excalidraw.md"
    excalidraw_content = """---
description: Generate Excalidraw diagram
argument-hint: [description]
---

Generate diagram: $ARGUMENTS

```bash
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "$ARGUMENTS"
```
"""
    excalidraw_cmd.write_text(excalidraw_content, encoding="utf-8")
    
    print(f"OK: Installed to Claude Code: {claude_md}, {commands_dir}/")
    return True


def install_windsurf(base_path: Path) -> bool:
    """Install skill to Windsurf IDE."""
    windsurf_dir = base_path / ".windsurf"
    windsurf_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = windsurf_dir / "rules.md"
    
    content = f"""# Windsurf Rules - open-python-skills

## Skill Location
The open-python-skills skill is located at `{SKILL_PATH}`.

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

### Search Scripts
```bash
# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"

# Get full entry
python3 .shared/scripts/knowledge_db.py --get entry-id

# List categories
python3 .shared/scripts/knowledge_db.py --list-categories
```

## Core Principles
1. Async-first for I/O operations
2. Use Pydantic for validations
3. Dependency injection with Depends()
4. Validate early, fail fast
5. Security by default
"""
    
    rules_file.write_text(content, encoding="utf-8")
    print(f"OK: Installed to Windsurf: {rules_file}")
    return True


def install_kiro(base_path: Path) -> bool:
    """Install skill to Kiro IDE."""
    kiro_dir = base_path / ".kiro"
    kiro_dir.mkdir(parents=True, exist_ok=True)
    
    rules_file = kiro_dir / "rules.md"
    
    content = f"""# Kiro Rules - open-python-skills

## Skill
This project includes the **open-python-skills** skill for Python backend development.

### Skill Entry Point
`{SKILL_PATH}`

### Knowledge Sources
1. **Knowledge Database** (`.shared/data/*.json`)
   - Incremental, searchable best practices and patterns

### Search Commands
```bash
# Knowledge database search
python3 .shared/scripts/knowledge_db.py "async routes"
python3 .shared/scripts/knowledge_db.py --get async-routes-io
python3 .shared/scripts/knowledge_db.py --list-categories
python3 .shared/scripts/knowledge_db.py --stats
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
    print(f"OK: Installed to Kiro: {rules_file}")
    return True


def install_copilot(base_path: Path) -> bool:
    """Install skill to GitHub Copilot."""
    copilot_dir = base_path / ".github" / "copilot"
    copilot_dir.mkdir(parents=True, exist_ok=True)
    
    instructions_file = copilot_dir / "instructions.md"
    
    content = f"""# GitHub Copilot Instructions - open-python-skills

## Skill Overview
This project uses the **open-python-skills** knowledge base for Python backend development best practices.

### Skill Location
- Main skill file: `{SKILL_PATH}`
- Knowledge database: `.shared/data/` (JSON files)
- Search scripts: `.shared/scripts/`

### Search Commands
```bash
python3 .shared/scripts/knowledge_db.py "query"
python3 .shared/scripts/knowledge_db.py --get entry-id
python3 .shared/scripts/knowledge_db.py --list-categories
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
    print(f"OK: Installed to GitHub Copilot: {instructions_file}")
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
- Knowledge Database: `.shared/data/*.json`
- Search Scripts: `.shared/scripts/*.py`

### Usage
```bash
# Search knowledge database
python3 .shared/scripts/knowledge_db.py "query"
python3 .shared/scripts/knowledge_db.py --get entry-id
python3 .shared/scripts/knowledge_db.py --list-categories
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
    print(f"OK: Installed to Antigravity: {agents_file}")
    return True


def load_all_databases() -> list:
    """Load all JSON databases from python-backend skill."""
    entries = []
    
    # Try package path first
    data_path = get_package_skill_path("python-backend") / "data"
    
    if not data_path.exists():
        # Try local .shared path
        data_path = Path.cwd() / ".shared" / "python-backend" / "data"

    if not data_path.exists():
        print("ERROR: Data directory not found")
        return entries

    for json_file in data_path.glob("*.json"):
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
                if "entries" in data:
                    entries.extend(data["entries"])
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Failed to load {json_file}: {e}", file=sys.stderr)
    
    return entries


def cmd_search(query: str, category: str | None = None) -> None:
    """Search knowledge database."""
    entries = load_all_databases()
    
    if not entries:
        print("No entries found. Run 'open-python-skills init' first.")
        return
    
    query_lower = query.lower()
    results = []
    
    for entry in entries:
        # Filter by category
        if category and entry.get("category", "").lower() != category.lower():
            continue
        
        # Search in title, summary, tags, content
        searchable = " ".join([
            entry.get("title", ""),
            entry.get("summary", ""),
            " ".join(entry.get("tags", [])),
            entry.get("content", ""),
        ]).lower()
        
        if query_lower in searchable:
            results.append(entry)
    
    if not results:
        print(f"No results for '{query}'")
        return
    
    print(f"\nFound {len(results)} result(s) for '{query}':\n")
    for entry in results[:10]:
        print(f"  [{entry.get('id')}] {entry.get('title')}")
        print(f"      {entry.get('summary', '')[:80]}...")
        print()


def cmd_get(entry_id: str) -> None:
    """Get full entry by ID."""
    entries = load_all_databases()
    
    for entry in entries:
        if entry.get("id") == entry_id:
            print(f"\n{'='*60}")
            print(f"ID: {entry.get('id')}")
            print(f"Title: {entry.get('title')}")
            print(f"Category: {entry.get('category')}")
            print(f"Tags: {', '.join(entry.get('tags', []))}")
            print(f"{'='*60}\n")
            print(f"Summary:\n{entry.get('summary', '')}\n")
            print(f"Content:\n{entry.get('content', '')}\n")
            
            if "code_examples" in entry:
                print("Code Examples:")
                for i, example in enumerate(entry["code_examples"], 1):
                    print(f"\n--- Example {i}: {example.get('description', '')} ---")
                    print(example.get("code", ""))
            return
    
    print(f"Entry '{entry_id}' not found.")


def cmd_categories() -> None:
    """List all categories."""
    entries = load_all_databases()
    
    categories = {}
    for entry in entries:
        cat = entry.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nCategories:\n")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count} entries")


def cmd_stats() -> None:
    """Show statistics."""
    entries = load_all_databases()
    
    categories = {}
    tags = set()
    
    for entry in entries:
        cat = entry.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1
        tags.update(entry.get("tags", []))
    
    print(f"\n{'='*60}")
    print("Open Python Skills - Statistics")
    print(f"{'='*60}\n")
    print(f"Total entries: {len(entries)}")
    print(f"Categories: {len(categories)}")
    print(f"Unique tags: {len(tags)}")
    print("\nBy category:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description="Open Python Skills - AI skill for Python backend development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  open-python-skills init --all          Install to all AI assistants
  open-python-skills init --cursor       Install to Cursor only
  open-python-skills search "redis"      Search for redis patterns
  open-python-skills get upstash-redis-init  Get full entry
  open-python-skills categories          List all categories
  open-python-skills stats               Show statistics
"""
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # init command
    init_parser = subparsers.add_parser("init", help="Initialize skill installation")
    init_parser.add_argument("--cursor", action="store_true", help="Install to Cursor")
    init_parser.add_argument("--claude", action="store_true", help="Install to Claude Code")
    init_parser.add_argument("--windsurf", action="store_true", help="Install to Windsurf")
    init_parser.add_argument("--kiro", action="store_true", help="Install to Kiro")
    init_parser.add_argument("--copilot", action="store_true", help="Install to GitHub Copilot")
    init_parser.add_argument("--antigravity", action="store_true", help="Install to Antigravity")
    init_parser.add_argument("--all", action="store_true", help="Install to all assistants")
    
    # search command
    search_parser = subparsers.add_parser("search", help="Search knowledge database")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--category", "-c", help="Filter by category")
    
    # get command
    get_parser = subparsers.add_parser("get", help="Get full entry by ID")
    get_parser.add_argument("entry_id", help="Entry ID")
    
    # categories command
    subparsers.add_parser("categories", help="List all categories")
    
    # stats command
    subparsers.add_parser("stats", help="Show statistics")
    
    # version
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.version:
        from open_python_skills import __version__
        print(f"open-python-skills v{__version__}")
        return
    
    if args.command == "search":
        cmd_search(args.query, args.category)
        return
    
    if args.command == "get":
        cmd_get(args.entry_id)
        return
    
    if args.command == "categories":
        cmd_categories()
        return
    
    if args.command == "stats":
        cmd_stats()
        return
    
    if args.command == "init":
        base_path = get_target_path()
        
        # First, copy .shared files
        if not copy_shared_files(base_path):
            sys.exit(1)
        
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
            print("ERROR: No IDE specified!")
            print("   Use --cursor, --claude, --windsurf, --kiro, --copilot, --antigravity, or --all")
            sys.exit(1)
        
        print(f"\nInstalling {SKILL_NAME} to {len(installers)} IDE(s)...\n")
        
        for name, installer_func in installers:
            total_count += 1
            try:
                if installer_func(base_path):
                    success_count += 1
            except OSError as e:
                print(f"ERROR: Failed to install to {name}: {e}", file=sys.stderr)
        
        print(f"\n{'='*60}")
        print(f"Successfully installed to {success_count}/{total_count} IDE(s)")
        print(f"{'='*60}\n")
        print("Next steps:")
        print("  1. Open your project in your AI-powered IDE")
        print("  2. The skill will be automatically detected")
        print("  3. Use knowledge base: python3 .shared/scripts/knowledge_db.py 'query'")
        return
    
    # No command specified
    parser.print_help()


def main_entry():
    """Entry point for console script."""
    main()


if __name__ == "__main__":
    main()
