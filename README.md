# Open Python Skills CLI

Command-line tool to install Python Backend Pro Max skill to different AI assistants (Cursor, Claude Code, Windsurf, Kiro, GitHub Copilot, Antigravity).

## Installation

```bash
pip install open-python-skills
```

## Quick Start

```bash
# Install to Cursor
open-python-skills init --cursor

# Install to all IDEs
open-python-skills init --all
```

## Usage

```bash
# Install to specific IDE
open-python-skills init --cursor      # Cursor
open-python-skills init --claude      # Claude Code
open-python-skills init --windsurf    # Windsurf
open-python-skills init --kiro        # Kiro
open-python-skills init --copilot     # GitHub Copilot
open-python-skills init --antigravity # Antigravity

# Install to multiple IDEs
open-python-skills init --cursor --claude --windsurf

# Install to all IDEs
open-python-skills init --all
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
│   └── references/
└── ...
```

## Environment Variables

You can specify the project path using:

```bash
export OPEN_PYTHON_SKILLS_PROJECT="/path/to/project"
open-python-skills init --cursor
```

## Development

```bash
# Install in development mode
pip install -e .

# Run tests
python -m pytest
```

## License

MIT
