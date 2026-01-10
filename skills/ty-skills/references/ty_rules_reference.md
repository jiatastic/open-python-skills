# ty Rules Reference

Complete reference for all ty rules and their configuration.

## Rule Severity Levels

| Level | Behavior |
|-------|----------|
| `error` | Reported as error, ty exits with code 1 |
| `warn` | Reported as warning, ty exits with code 0 (unless `--error-on-warning`) |
| `ignore` | Rule completely disabled |

## Configuration

### Via pyproject.toml

```toml
[tool.ty.rules]
possibly-unresolved-reference = "error"
division-by-zero = "warn"
unused-ignore-comment = "ignore"
```

### Via ty.toml

```toml
[rules]
possibly-unresolved-reference = "error"
division-by-zero = "warn"
```

### Via CLI

```bash
ty check --error possibly-unresolved-reference --warn division-by-zero
```

---

## Error Rules (Critical)

### possibly-unresolved-reference

**Default:** error  
**Description:** Variable might not be defined in all code paths.

```python
# ❌ Error
def greet(condition: bool) -> str:
    if condition:
        name = "World"
    return f"Hello, {name}"  # 'name' possibly unbound

# ✅ Fix
def greet(condition: bool) -> str:
    name = "Guest"  # Default value
    if condition:
        name = "World"
    return f"Hello, {name}"
```

### invalid-argument-type

**Default:** error  
**Description:** Argument type doesn't match the expected parameter type.

```python
# ❌ Error
def greet(name: str) -> str:
    return f"Hello, {name}"

greet(123)  # Expected str, got int

# ✅ Fix
greet("World")
# or
greet(str(123))
```

### incompatible-assignment

**Default:** error  
**Description:** Assigned value is incompatible with the declared type.

```python
# ❌ Error
x: int = "hello"

# ✅ Fix
x: int = 42
# or
x: str = "hello"
```

### missing-argument

**Default:** error  
**Description:** Required argument not provided to function call.

```python
# ❌ Error
def create_user(name: str, email: str) -> dict:
    return {"name": name, "email": email}

create_user("Alice")  # Missing 'email'

# ✅ Fix
create_user("Alice", "alice@example.com")
# or make email optional
def create_user(name: str, email: str | None = None) -> dict:
    ...
```

### unsupported-operator

**Default:** error  
**Description:** Operator not supported for the given types.

```python
# ❌ Error
"hello" + 42  # Can't add str and int

# ✅ Fix
"hello" + str(42)
```

### invalid-return-type

**Default:** error  
**Description:** Return value doesn't match declared return type.

```python
# ❌ Error
def get_count() -> int:
    return "42"  # Returns str, expected int

# ✅ Fix
def get_count() -> int:
    return 42
```

### possibly-unbound-import

**Default:** error  
**Description:** Import might fail at runtime.

```python
# ❌ Error
try:
    import optional_package
except ImportError:
    pass

optional_package.do_something()  # Might not be defined

# ✅ Fix
try:
    import optional_package
    HAS_OPTIONAL = True
except ImportError:
    optional_package = None
    HAS_OPTIONAL = False

if HAS_OPTIONAL and optional_package:
    optional_package.do_something()
```

---

## Warning Rules (Quality)

### division-by-zero

**Default:** warn  
**Description:** Potential division by zero detected.

```python
# ⚠️ Warning
def divide(a: int, b: int) -> float:
    return a / b  # b could be 0

# ✅ Fix
def divide(a: int, b: int) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

### unused-ignore-comment

**Default:** warn  
**Description:** Suppression comment is unnecessary.

```python
# ⚠️ Warning
x: int = 42  # type: ignore[incompatible-assignment]  # No error here!

# ✅ Fix - Remove unnecessary comment
x: int = 42
```

### redundant-cast

**Default:** warn  
**Description:** Type cast has no effect (value already has target type).

```python
from typing import cast

# ⚠️ Warning
x: int = 42
y = cast(int, x)  # x is already int

# ✅ Fix
y = x
```

### possibly-unbound-attribute

**Default:** warn  
**Description:** Attribute might not exist on the object.

```python
# ⚠️ Warning
def process(obj: Animal | None) -> str:
    return obj.name  # obj could be None

# ✅ Fix
def process(obj: Animal | None) -> str:
    if obj is None:
        return "Unknown"
    return obj.name
```

### index-out-of-bounds

**Default:** warn  
**Description:** Index might be out of range.

```python
# ⚠️ Warning
def get_first(items: list[int]) -> int:
    return items[0]  # Empty list would fail

# ✅ Fix
def get_first(items: list[int]) -> int | None:
    return items[0] if items else None
```

### possibly-missing-attribute

**Default:** warn  
**Description:** Attribute access might fail.

### possibly-missing-import

**Default:** warn  
**Description:** Module might not be importable.

---

## Suppression Comments

### Suppress Single Rule

```python
x: int = "hello"  # type: ignore[incompatible-assignment]
```

### Suppress Multiple Rules

```python
result = risky()  # type: ignore[possibly-unresolved-reference, invalid-argument-type]
```

### Suppress All (Not Recommended)

```python
legacy_result = legacy_code()  # type: ignore
```

### File-Level Suppression

```python
# ty: ignore[possibly-unbound-attribute]
# This comment at the top suppresses the rule for the entire file
```

---

## Per-File Overrides

```toml
# Relaxed rules for tests
[[tool.ty.overrides]]
include = ["tests/**"]

[tool.ty.overrides.rules]
possibly-unresolved-reference = "warn"
invalid-argument-type = "warn"

# Strict rules for critical code
[[tool.ty.overrides]]
include = ["src/payments/**", "src/auth/**"]

[tool.ty.overrides.rules]
division-by-zero = "error"
possibly-unbound-attribute = "error"
```

---

## Gradual Adoption Strategy

### Phase 1: Critical Errors Only

```toml
[tool.ty.rules]
# Start with only truly critical errors
division-by-zero = "error"
invalid-argument-type = "warn"
incompatible-assignment = "warn"

# Disable noisy rules initially
possibly-unresolved-reference = "ignore"
redundant-cast = "ignore"
```

### Phase 2: Enable Warnings

```toml
[tool.ty.rules]
division-by-zero = "error"
invalid-argument-type = "error"
incompatible-assignment = "error"
possibly-unresolved-reference = "warn"
unused-ignore-comment = "warn"
```

### Phase 3: Full Strictness

```toml
[tool.ty.rules]
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
incompatible-assignment = "error"
missing-argument = "error"
unsupported-operator = "error"
division-by-zero = "error"
unused-ignore-comment = "warn"
redundant-cast = "warn"

[tool.ty.terminal]
error-on-warning = true
```
