# Open Python Skills CLI

Command-line tool to install open-python-skills (a Python backend best-practices skill) to different AI assistants (Cursor, Claude Code, Windsurf, Kiro, GitHub Copilot, Antigravity).

## Installation

No installation needed! Just use `uvx` to run directly:

```bash
uvx open-python-skills init --cursor
```

## Quick Start

```bash
# Run directly with uvx (no installation needed)
uvx open-python-skills init --cursor

# Install to all IDEs
uvx open-python-skills init --all
```

## Usage

Use `uvx` to run commands directly:

```bash
# Install to specific IDE
uvx open-python-skills init --cursor      # Cursor
uvx open-python-skills init --claude      # Claude Code
uvx open-python-skills init --windsurf    # Windsurf
uvx open-python-skills init --kiro        # Kiro
uvx open-python-skills init --copilot     # GitHub Copilot
uvx open-python-skills init --antigravity # Antigravity

# Install to multiple IDEs
uvx open-python-skills init --cursor --claude --windsurf

# Install to all IDEs
uvx open-python-skills init --all
```

## Requirements

- Python 3.13+
- Project directory with `.shared/` folder
- Write permissions for creating IDE config files

## Project Structure

The CLI tool expects a project structure like:

```
your-project/
├── .shared/
│   ├── SKILL.md
│   ├── scripts/
│   ├── data/
└── ...
```

## Environment Variables

You can specify the project path using:

```bash
export OPEN_PYTHON_SKILLS_PROJECT="/path/to/project"
uvx open-python-skills init --cursor
```

## License

MIT
