---
name: commit-message
description: >
  Analyze git changes and generate conventional commit messages. Supports batch commits
  for multiple unrelated changes. Use when: (1) Creating git commits, (2) Reviewing
  staged changes, (3) Splitting large changesets into logical commits.
---

# commit-message

Analyze git changes and generate context-aware commit messages following Conventional Commits.

## Quick Start

```bash
# Analyze all changes
python3 .shared/commit-message/scripts/analyze_changes.py --analyze

# Get batch commit suggestions
python3 .shared/commit-message/scripts/analyze_changes.py --batch

# Generate message for specific files
python3 .shared/commit-message/scripts/analyze_changes.py --generate "src/api/*.py"
```

## Commands

| Command | Description |
|---------|-------------|
| `--analyze` | Show all changed files with status and categories |
| `--batch` | Suggest how to split changes into multiple commits |
| `--generate [pattern]` | Generate commit message for matching files |
| `--staged` | Only analyze staged changes (default: all changes) |

## Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(api): add user authentication` |
| `fix` | Bug fix | `fix(db): resolve connection timeout` |
| `refactor` | Code restructuring | `refactor(utils): simplify helper functions` |
| `docs` | Documentation | `docs: update README` |
| `test` | Tests | `test(api): add user endpoint tests` |
| `chore` | Maintenance | `chore: update dependencies` |
| `style` | Formatting | `style: fix linting errors` |

## Batch Commit Workflow

When you have multiple unrelated changes:

1. Run `--batch` to see suggested commit groups
2. Stage files for first commit: `git add <files>`
3. Commit with suggested message
4. Repeat for remaining groups

## Grouping Strategy

Files are grouped by:
- **Directory/Module**: `src/api/`, `tests/`, `docs/`
- **Change Type**: Added vs Modified vs Deleted
- **Semantic Relationship**: Related files together
