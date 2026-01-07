# VS Code Setup for ty

Configure ty as your Python type checker in VS Code.

## Installation

### 1. Install ty Extension

Search for "ty" in the VS Code extensions marketplace, or:

```bash
code --install-extension astral-sh.ty
```

### 2. Install ty CLI

```bash
# Using uv (recommended)
uv tool install ty

# Or with pip
pip install ty
```

## Configuration

### settings.json

```json
{
  // Enable ty
  "ty.enable": true,
  
  // Path to ty executable (optional, auto-detected)
  "ty.path": "",
  
  // Path to configuration file (optional)
  "ty.configPath": "./pyproject.toml",
  
  // Disable Pylance type checking (to avoid conflicts)
  "python.analysis.typeCheckingMode": "off",
  
  // Or disable Pylance entirely
  "python.languageServer": "None"
}
```

### Workspace Settings

Create `.vscode/settings.json` in your project:

```json
{
  "ty.enable": true,
  "ty.configPath": "${workspaceFolder}/pyproject.toml",
  
  // Disable Pylance type checking
  "python.analysis.typeCheckingMode": "off",
  
  // Keep Pylance for other features (completion, etc.)
  "python.languageServer": "Pylance"
}
```

## Features

### Diagnostics

ty provides inline diagnostics as you type:

- **Errors** (red squiggles) - Critical type issues
- **Warnings** (yellow squiggles) - Code quality issues
- **Hints** (blue dots) - Suggestions

### Hover Information

Hover over variables to see:

- Inferred type
- Documentation
- Type narrowing context

### Go to Definition

- `Ctrl+Click` / `Cmd+Click` on a symbol
- `F12` for Go to Definition
- `Ctrl+F12` / `Cmd+F12` for Go to Type Definition

### Find References

- `Shift+F12` to find all references
- Right-click → "Find All References"

### Code Actions

- Quick fixes for type errors
- Auto-import suggestions
- Type annotation helpers

## Keyboard Shortcuts

| Action | Windows/Linux | macOS |
|--------|---------------|-------|
| Go to Definition | `F12` | `F12` |
| Peek Definition | `Alt+F12` | `Option+F12` |
| Find References | `Shift+F12` | `Shift+F12` |
| Quick Fix | `Ctrl+.` | `Cmd+.` |
| Rename Symbol | `F2` | `F2` |

## Recommended Extensions

For the best experience with ty:

```json
{
  "recommendations": [
    "astral-sh.ty",
    "charliermarsh.ruff",  // Ruff for linting/formatting
    "ms-python.python"     // Python extension (for debugging, etc.)
  ]
}
```

## Troubleshooting

### ty not found

If VS Code can't find ty:

```json
{
  "ty.path": "/path/to/ty"
}
```

Find the path with:

```bash
which ty
# or
uv tool dir
```

### Conflicts with Pylance

If you see duplicate diagnostics:

```json
{
  // Option 1: Disable Pylance type checking
  "python.analysis.typeCheckingMode": "off",
  
  // Option 2: Use ty as the only type checker
  "python.languageServer": "None",
  "ty.enable": true
}
```

### Performance Issues

For large projects:

```json
{
  // Exclude large directories
  "ty.exclude": [
    "**/node_modules",
    "**/.venv",
    "**/build"
  ]
}
```

### Wrong Python Version

Ensure ty uses the correct Python:

```toml
# pyproject.toml
[tool.ty.environment]
python-version = "3.11"
python = "./.venv"
```

## Tasks

Add ty to VS Code tasks:

```json
// .vscode/tasks.json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "ty: Check",
      "type": "shell",
      "command": "ty check",
      "group": "build",
      "problemMatcher": {
        "owner": "ty",
        "pattern": {
          "regexp": "^(.+):(\\d+):(\\d+): (error|warning): (.+)$",
          "file": 1,
          "line": 2,
          "column": 3,
          "severity": 4,
          "message": 5
        }
      }
    }
  ]
}
```

Run with `Ctrl+Shift+B` (or `Cmd+Shift+B` on macOS).
