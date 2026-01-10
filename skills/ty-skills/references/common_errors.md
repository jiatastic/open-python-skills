# Common ty Errors and Solutions

Practical solutions for frequently encountered ty type errors.

---

## possibly-unresolved-reference

**Error:** Variable might not be defined in all code paths.

### Example 1: Conditional Assignment

```python
# ❌ Error
def get_status(success: bool) -> str:
    if success:
        message = "OK"
    return message  # 'message' possibly unresolved

# ✅ Solution 1: Default value
def get_status(success: bool) -> str:
    message = "FAILED"
    if success:
        message = "OK"
    return message

# ✅ Solution 2: Early return
def get_status(success: bool) -> str:
    if success:
        return "OK"
    return "FAILED"
```

### Example 2: Loop Variable

```python
# ❌ Error
def find_first(items: list[int], target: int) -> int:
    for item in items:
        if item == target:
            found = item
            break
    return found  # 'found' possibly unresolved

# ✅ Solution
def find_first(items: list[int], target: int) -> int | None:
    for item in items:
        if item == target:
            return item
    return None
```

### Example 3: Exception Handling

```python
# ❌ Error
def parse_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError:
        pass
    return result  # 'result' possibly unresolved

# ✅ Solution
def parse_int(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
```

---

## invalid-argument-type

**Error:** Argument type doesn't match the expected parameter type.

### Example 1: Wrong Type

```python
# ❌ Error
def greet(name: str) -> str:
    return f"Hello, {name}"

greet(123)  # Expected str, got int

# ✅ Solution: Convert or fix call site
greet(str(123))
greet("World")
```

### Example 2: None Where Not Expected

```python
# ❌ Error
def process(data: str) -> str:
    return data.upper()

value: str | None = get_value()
process(value)  # Might be None

# ✅ Solution: Check for None
if value is not None:
    process(value)

# Or use default
process(value or "default")
```

### Example 3: List vs Single Item

```python
# ❌ Error
def process_item(item: str) -> None:
    print(item)

items = ["a", "b", "c"]
process_item(items)  # Expected str, got list[str]

# ✅ Solution: Iterate or fix function signature
for item in items:
    process_item(item)
```

---

## incompatible-assignment

**Error:** Assigned value is incompatible with the declared type.

### Example 1: Type Mismatch

```python
# ❌ Error
x: int = "hello"

# ✅ Solution: Fix type or value
x: int = 42
# or
x: str = "hello"
```

### Example 2: Narrowing Issue

```python
# ❌ Error
values: list[int] = [1, 2, 3]
values = None  # list[int] can't be None

# ✅ Solution: Adjust type
values: list[int] | None = [1, 2, 3]
values = None
```

### Example 3: Dict Type Mismatch

```python
# ❌ Error
config: dict[str, int] = {"name": "test"}  # "test" is str, not int

# ✅ Solution
config: dict[str, str | int] = {"name": "test"}
# or
config: dict[str, str] = {"name": "test"}
```

---

## missing-argument

**Error:** Required argument not provided to function call.

### Example 1: Missing Positional

```python
# ❌ Error
def create_user(name: str, email: str) -> dict:
    return {"name": name, "email": email}

create_user("Alice")  # Missing 'email'

# ✅ Solution 1: Provide the argument
create_user("Alice", "alice@example.com")

# ✅ Solution 2: Make optional
def create_user(name: str, email: str | None = None) -> dict:
    return {"name": name, "email": email}
```

### Example 2: Missing Keyword

```python
# ❌ Error
def connect(host: str, port: int, timeout: int) -> Connection:
    ...

connect("localhost", 8080)  # Missing 'timeout'

# ✅ Solution: Add default
def connect(host: str, port: int, timeout: int = 30) -> Connection:
    ...
```

---

## unsupported-operator

**Error:** Operator not supported for the given types.

### Example 1: Type Incompatibility

```python
# ❌ Error
result = "hello" + 42  # Can't add str and int

# ✅ Solution
result = "hello" + str(42)
```

### Example 2: None Type

```python
# ❌ Error
value: int | None = get_value()
result = value + 10  # Can't add None and int

# ✅ Solution
if value is not None:
    result = value + 10
# or
result = (value or 0) + 10
```

### Example 3: Custom Class

```python
# ❌ Error
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

p1 = Point(1, 2)
p2 = Point(3, 4)
p3 = p1 + p2  # Point doesn't support +

# ✅ Solution: Implement __add__
class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)
```

---

## division-by-zero

**Error:** Potential division by zero detected.

```python
# ⚠️ Warning
def average(numbers: list[int]) -> float:
    return sum(numbers) / len(numbers)  # len could be 0

# ✅ Solution 1: Check first
def average(numbers: list[int]) -> float:
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

# ✅ Solution 2: Raise exception
def average(numbers: list[int]) -> float:
    if not numbers:
        raise ValueError("Cannot average empty list")
    return sum(numbers) / len(numbers)
```

---

## possibly-unbound-attribute

**Error:** Attribute might not exist on the object.

### Example 1: Optional Object

```python
# ⚠️ Warning
user: User | None = get_user(id)
print(user.name)  # user could be None

# ✅ Solution
if user is not None:
    print(user.name)
# or
print(user.name if user else "Unknown")
```

### Example 2: Union Types

```python
# ⚠️ Warning
class Dog:
    name: str

class Cat:
    nickname: str

def get_name(pet: Dog | Cat) -> str:
    return pet.name  # Cat doesn't have 'name'

# ✅ Solution 1: Check type
def get_name(pet: Dog | Cat) -> str:
    if isinstance(pet, Dog):
        return pet.name
    return pet.nickname

# ✅ Solution 2: Common interface
class Pet(Protocol):
    @property
    def display_name(self) -> str: ...

def get_name(pet: Pet) -> str:
    return pet.display_name
```

---

## redundant-cast

**Error:** Type cast has no effect (value already has target type).

```python
from typing import cast

# ⚠️ Warning
x: int = 42
y = cast(int, x)  # x is already int

# ✅ Solution: Remove cast
y = x

# Note: cast is only needed when you know more than the type checker
data: object = get_json()
if is_user_dict(data):
    user = cast(dict[str, str], data)  # Valid: narrowing from object
```

---

## unused-ignore-comment

**Error:** Suppression comment is unnecessary.

```python
# ⚠️ Warning
x: int = 42  # type: ignore[incompatible-assignment]  # No error here!

# ✅ Solution: Remove the comment
x: int = 42
```

---

## Pattern: Fixing Multiple Errors at Once

When you have many related errors, fix the root cause:

```python
# ❌ Many errors
def process_data(data):  # No type hints
    result = data.split(",")  # Unknown methods
    for item in result:
        handle(item)  # Unknown function

# ✅ Add types to fix multiple errors at once
def process_data(data: str) -> None:
    result: list[str] = data.split(",")
    for item in result:
        handle(item)

def handle(item: str) -> None:
    print(item.strip())
```

---

## Debugging Tips

### 1. Use reveal_type

```python
x = some_complex_expression()
reveal_type(x)  # ty will show the inferred type
```

### 2. Run with Full Output

```bash
ty check --output-format full
```

### 3. Check Specific Files

```bash
ty check src/problematic_file.py
```

### 4. Ignore Temporarily

```python
# Fix later, don't block CI now
result = legacy_function()  # type: ignore[possibly-unresolved-reference]
```
