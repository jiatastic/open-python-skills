# Cursor Setup for ty

Configure ty as your Python type checker in Cursor.

## Installation

### 1. ty Integration

Cursor has built-in support for ty. Enable it in settings:

1. Open Settings (`Cmd+,` / `Ctrl+,`)
2. Search for "ty"
3. Enable "Ty: Enable"

### 2. Install ty CLI

```bash
# Using uv (recommended)
uv tool install ty

# Or with pip
pip install ty
```

## Configuration

### settings.json

Open Settings → JSON and add:

```json
{
  // Enable ty
  "ty.enable": true,
  
  // Use project configuration
  "ty.configPath": "${workspaceFolder}/pyproject.toml",
  
  // Disable built-in type checking to avoid conflicts
  "python.analysis.typeCheckingMode": "off"
}
```

### Project Configuration

Create or update `pyproject.toml`:

```toml
[tool.ty.environment]
python-version = "3.11"
python = "./.venv"

[tool.ty.rules]
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
unused-ignore-comment = "warn"

[tool.ty.src]
include = ["src", "tests"]
```

## Features

### Real-time Type Checking

ty checks your code as you type, showing:

- **Errors** - Red underlines for type violations
- **Warnings** - Yellow underlines for potential issues
- **Inlay Hints** - Inline type annotations

### AI-Powered Fixes

Cursor's AI can help fix type errors:

1. Hover over a type error
2. Click "Fix with AI" or use `Cmd+K` / `Ctrl+K`
3. AI suggests a typed solution

### Type-Aware Completions

ty enhances Cursor's autocomplete with:

- Type-accurate suggestions
- Method signatures with types
- Parameter hints

## Keyboard Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Go to Definition | `Cmd+Click` | `Ctrl+Click` |
| Type Definition | `Cmd+F12` | `Ctrl+F12` |
| Find References | `Shift+F12` | `Shift+F12` |
| Quick Fix | `Cmd+.` | `Ctrl+.` |
| AI Fix | `Cmd+K` | `Ctrl+K` |

## Recommended Settings

```json
{
  // ty settings
  "ty.enable": true,
  "ty.configPath": "${workspaceFolder}/pyproject.toml",
  
  // Disable conflicting features
  "python.analysis.typeCheckingMode": "off",
  
  // Enable inlay hints
  "editor.inlayHints.enabled": "on",
  
  // Ruff for formatting (pairs well with ty)
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

## Using ty with Cursor AI

### Type Error Fixes

When you see a type error:

1. Select the error line
2. Press `Cmd+K` / `Ctrl+K`
3. Ask: "Fix this type error"

Cursor AI understands ty's error messages and can suggest typed fixes.

### Generate Type Annotations

Select untyped code and ask:

- "Add type annotations to this function"
- "What should the types be here?"
- "Make this code type-safe"

### Explain Type Errors

Ask Cursor AI to explain:

- "Why is this a type error?"
- "What type does ty expect here?"
- "How do I fix this incompatible-assignment error?"

## Troubleshooting

### ty not detecting project

Ensure `pyproject.toml` or `ty.toml` is in the workspace root:

```bash
# Check if ty can find your config
ty check --show-config
```

### Slow Performance

For large projects, exclude unnecessary directories:

```toml
# pyproject.toml
[tool.ty.src]
exclude = [
  "**/node_modules",
  "**/.venv",
  "**/build",
  "**/dist"
]
```

### Conflicts with Other Type Checkers

Disable other Python type checkers:

```json
{
  "python.analysis.typeCheckingMode": "off",
  "mypy.enabled": false,
  "pylint.enabled": false
}
```

## Integration with Cursor Rules

Add ty-aware rules to `.cursorrules`:

```markdown
# Type Checking

- All Python code must be type-safe with ty
- Use type annotations for function parameters and returns
- Fix type errors before committing
- Use `reveal_type()` to debug type inference
```
