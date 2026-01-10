# PROJECT KNOWLEDGE BASE

**Generated:** 2026-01-10 01:07 ET
**Commit:** c82be43
**Branch:** main

## OVERVIEW
Python CLI package that installs AI editor skills and ships bundled knowledge content.

## STRUCTURE
```
agent_email/
├── open_python_skills/           # package + bundled skills
├── README.md                     # usage and CLI commands
├── pyproject.toml                # package metadata + entrypoint
└── repo_architecture.excalidraw  # architecture diagram (Excalidraw JSON)
```

## WHERE TO LOOK
| Task | Location | Notes |
|------|----------|-------|
| CLI entrypoint | `open_python_skills/cli.py` | install + search/get/categories/stats |
| Package metadata | `pyproject.toml` | console script + build config |
| Skill catalog | `open_python_skills/*/SKILL.md` | skill descriptions + usage |
| End-user usage | `README.md` | quick start + commands |

## CONVENTIONS
- Skills are packaged under `open_python_skills/<skill>/` with a `SKILL.md` front-matter header.
- Skill content uses `references/` for markdown, `data/` for JSON, `assets/` for Excalidraw libraries.
- CLI entrypoint is `open_python_skills.cli:main_entry`.

## ANTI-PATTERNS (THIS PROJECT)
- Avoid committing secrets; `.env` contains a PyPI token.
- Do not edit generated install outputs (`.shared`, `.cursor`, `.claude`, `.windsurf`, `.kiro`, `.github/copilot`) in target projects; source of truth is `open_python_skills/`.

## UNIQUE STYLES
- CLI installs skill bundles into `.shared/` and writes IDE-specific command/rules files.

## COMMANDS
```bash
open-python-skills init --cursor
open-python-skills init --claude
open-python-skills init --windsurf
open-python-skills init --kiro
open-python-skills init --copilot
open-python-skills init --all
open-python-skills search "query"
open-python-skills get <entry-id>
open-python-skills categories
open-python-skills stats
```

## NOTES
- `open_python_skills/__init__.py` version differs from `pyproject.toml`; keep them in sync for releases.
