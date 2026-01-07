# Migration Guide: mypy/pyright → ty

Complete guide for migrating from mypy or pyright to ty.

## Why Migrate to ty?

| Feature | mypy | pyright | ty |
|---------|------|---------|-----|
| Speed | Slow | Fast | **10-100x faster** |
| Language Server | Basic | Good | **Excellent** |
| Intersection Types | ❌ | ❌ | **✅ First-class** |
| Incremental Analysis | Basic | Good | **Fine-grained** |
| Error Messages | Basic | Good | **Rich contextual** |
| Rust-based | ❌ | ❌ | **✅** |

---

## Quick Migration Steps

### 1. Install ty

```bash
# Using uv (recommended)
uv tool install ty

# Or with pip
pip install ty

# Verify installation
ty --version
```

### 2. Run Initial Check

```bash
# Check your project
ty check

# Get verbose output
ty check --output-format full
```

### 3. Create Configuration

```bash
# ty will use pyproject.toml or ty.toml
# See configuration section below
```

---

## Configuration Migration

### From mypy.ini

**mypy.ini:**
```ini
[mypy]
python_version = 3.11
strict = true
ignore_missing_imports = true
disallow_untyped_defs = true
disallow_any_generics = true

[mypy-tests.*]
disallow_untyped_defs = false
```

**Equivalent ty (pyproject.toml):**
```toml
[tool.ty.environment]
python-version = "3.11"

[tool.ty.rules]
# ty doesn't have a "strict" mode - configure individual rules
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
incompatible-assignment = "error"
missing-argument = "error"

[tool.ty.src]
include = ["src", "tests"]

# Relaxed rules for tests
[[tool.ty.overrides]]
include = ["tests/**"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
```

### From pyrightconfig.json

**pyrightconfig.json:**
```json
{
  "include": ["src"],
  "exclude": ["**/node_modules", "**/__pycache__"],
  "pythonVersion": "3.11",
  "pythonPlatform": "Linux",
  "typeCheckingMode": "strict",
  "reportMissingImports": "error",
  "reportUnusedImport": "warning"
}
```

**Equivalent ty (pyproject.toml):**
```toml
[tool.ty.environment]
python-version = "3.11"
python-platform = "linux"

[tool.ty.src]
include = ["src"]
exclude = ["**/node_modules", "**/__pycache__"]

[tool.ty.rules]
# Map pyright rules to ty rules
possibly-unresolved-reference = "error"
possibly-unbound-import = "error"
unused-ignore-comment = "warn"
```

---

## Rule Mapping

### mypy → ty

| mypy Error Code | ty Rule |
|-----------------|---------|
| `[arg-type]` | `invalid-argument-type` |
| `[return-value]` | `invalid-return-type` |
| `[assignment]` | `incompatible-assignment` |
| `[call-arg]` | `missing-argument` |
| `[operator]` | `unsupported-operator` |
| `[attr-defined]` | `possibly-unbound-attribute` |
| `[name-defined]` | `possibly-unresolved-reference` |
| `[import]` | `possibly-unbound-import` |
| `[unused-ignore]` | `unused-ignore-comment` |
| `[redundant-cast]` | `redundant-cast` |

### pyright → ty

| pyright Rule | ty Rule |
|--------------|---------|
| `reportArgumentType` | `invalid-argument-type` |
| `reportReturnType` | `invalid-return-type` |
| `reportAssignmentType` | `incompatible-assignment` |
| `reportCallIssue` | `missing-argument` |
| `reportOperatorIssue` | `unsupported-operator` |
| `reportAttributeAccessIssue` | `possibly-unbound-attribute` |
| `reportUndefinedVariable` | `possibly-unresolved-reference` |
| `reportMissingImports` | `possibly-unbound-import` |
| `reportUnusedIgnore` | `unused-ignore-comment` |
| `reportUnnecessaryCast` | `redundant-cast` |

---

## Comment Syntax Migration

### mypy comments

```python
# mypy
x: int = "hello"  # type: ignore[assignment]
y = data  # type: ignore[name-defined]
```

```python
# ty - same syntax works!
x: int = "hello"  # type: ignore[incompatible-assignment]
y = data  # type: ignore[possibly-unresolved-reference]
```

### pyright comments

```python
# pyright
x: int = "hello"  # pyright: ignore[reportAssignmentType]
y = data  # pyright: ignore
```

```python
# ty
x: int = "hello"  # type: ignore[incompatible-assignment]
y = data  # type: ignore
```

**Note:** ty uses `# type: ignore[rule-name]` syntax, same as mypy.

---

## Handling Differences

### 1. Strictness Modes

mypy and pyright have `--strict` modes. ty uses individual rule configuration:

```toml
# ty "strict" equivalent
[tool.ty.rules]
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
incompatible-assignment = "error"
missing-argument = "error"
unsupported-operator = "error"
division-by-zero = "error"
possibly-unbound-attribute = "error"
possibly-unbound-import = "error"

[tool.ty.terminal]
error-on-warning = true
```

### 2. Plugin System

mypy has plugins (e.g., `mypy-django`, `pydantic-mypy`). ty doesn't have plugins yet, but:

- Many patterns work without plugins due to better type inference
- Pydantic v2 has native typing support
- Django stubs work as-is

```toml
# Instead of mypy plugins, use extra-paths for stubs
[tool.ty.environment]
extra-paths = ["./typings", "./stubs"]
```

### 3. Custom Type Stubs

```toml
# mypy
[mypy]
mypy_path = stubs

# ty
[tool.ty.environment]
extra-paths = ["./stubs"]
```

### 4. Inline Type Comments

ty supports inline type comments for Python 2 compatibility:

```python
# Both work in ty
x = []  # type: list[int]
x: list[int] = []
```

---

## Gradual Migration Strategy

### Phase 1: Parallel Running

Run both type checkers during transition:

```yaml
# .github/workflows/ci.yml
jobs:
  typecheck:
    steps:
      - name: mypy (existing)
        run: mypy src/
        continue-on-error: true  # Don't block on mypy
      
      - name: ty (new)
        run: ty check src/
```

### Phase 2: ty as Primary

```yaml
jobs:
  typecheck:
    steps:
      - name: ty
        run: ty check src/
      
      # Optional: keep mypy for comparison
      - name: mypy (verification)
        run: mypy src/
        continue-on-error: true
```

### Phase 3: ty Only

```yaml
jobs:
  typecheck:
    steps:
      - name: ty
        run: ty check
```

---

## Common Migration Issues

### Issue 1: Different Error Locations

ty and mypy/pyright may report errors at different locations:

```python
def greet(name: str) -> str:
    return name

greet(123)  # mypy: error on this line
            # ty: also error here, but different message format
```

**Solution:** Focus on fixing the underlying issues, not matching line numbers.

### Issue 2: More/Fewer Errors

ty may catch errors that mypy/pyright miss (due to intersection types and better narrowing), or vice versa.

```python
# ty catches this due to better narrowing
def process(x: int | None) -> int:
    if x:
        return x
    # ty: error - missing return for x=0 case
```

**Solution:** These are usually real bugs. Fix them.

### Issue 3: Different Inference

```python
# mypy infers: list[Any]
# ty infers: list[int]
x = [1, 2, 3]
```

**Solution:** ty's inference is usually more precise. This rarely causes issues.

---

## CI/CD Updates

### GitHub Actions

```yaml
name: Type Check

on: [push, pull_request]

jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v4
      
      - name: Install ty
        run: uv tool install ty
      
      - name: Type check
        run: ty check
```

### Pre-commit Hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ty
        name: ty type check
        entry: ty check
        language: system
        types: [python]
        pass_filenames: false
```

---

## Editor Migration

### VS Code

Remove mypy/pylance extension, install ty extension:

```json
// .vscode/settings.json
{
  "python.analysis.typeCheckingMode": "off",  // Disable pylance type checking
  "ty.enable": true
}
```

### Cursor

ty is built into Cursor. Just configure:

```json
{
  "ty.enable": true,
  "ty.configPath": "./pyproject.toml"
}
```

See `editor_setup/` for more editor configurations.

---

## Cleanup Checklist

After successful migration:

- [ ] Remove `mypy.ini` or `pyrightconfig.json`
- [ ] Remove mypy/pyright from `requirements.txt` or `pyproject.toml`
- [ ] Update CI/CD configuration
- [ ] Update pre-commit hooks
- [ ] Update editor settings
- [ ] Update `# type: ignore` comments to use ty rule names
- [ ] Remove mypy plugins from configuration
- [ ] Update contributing guidelines
