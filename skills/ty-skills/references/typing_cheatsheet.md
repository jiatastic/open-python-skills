# Python Typing Cheatsheet

Quick reference for Python's `typing` module and type annotations.

## Basic Types

```python
# Primitives
x: int = 42
y: float = 3.14
z: str = "hello"
flag: bool = True
data: bytes = b"binary"
nothing: None = None
```

## Container Types (Python 3.9+)

```python
# Use lowercase built-in types
numbers: list[int] = [1, 2, 3]
mapping: dict[str, int] = {"a": 1, "b": 2}
unique: set[str] = {"a", "b"}
frozen: frozenset[int] = frozenset([1, 2])

# Tuple - fixed length
point: tuple[int, int] = (10, 20)

# Tuple - variable length
values: tuple[int, ...] = (1, 2, 3, 4)
```

## Optional and Union (Python 3.10+)

```python
# Optional (can be None)
name: str | None = None

# Union (one of multiple types)
id: int | str = "abc123"

# Pre-3.10 syntax (still valid)
from typing import Optional, Union
name: Optional[str] = None
id: Union[int, str] = "abc123"
```

## Callable Types

```python
from typing import Callable

# Function with no args returning int
getter: Callable[[], int]

# Function with args
adder: Callable[[int, int], int]

# Any callable
handler: Callable[..., None]

# Example
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)
```

## Type Aliases

```python
# Simple alias (Python 3.12+)
type UserId = int
type UserDict = dict[str, str | int]

# Pre-3.12 syntax
from typing import TypeAlias
UserId: TypeAlias = int
UserDict: TypeAlias = dict[str, str | int]
```

## Generics

### TypeVar

```python
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

# Constrained TypeVar
Number = TypeVar("Number", int, float)

def add(a: Number, b: Number) -> Number:
    return a + b
```

### Generic Classes

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()

# Usage
stack: Stack[int] = Stack()
stack.push(42)
```

### ParamSpec (Python 3.10+)

```python
from typing import ParamSpec, TypeVar, Callable

P = ParamSpec("P")
R = TypeVar("R")

def with_logging(func: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## Protocols (Structural Subtyping)

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

# Circle is a Drawable even without explicit inheritance
def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # ✅ Works
```

### Runtime Checkable Protocol

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Sized(Protocol):
    def __len__(self) -> int: ...

# Can use with isinstance
items = [1, 2, 3]
if isinstance(items, Sized):
    print(len(items))
```

## Type Guards

### TypeGuard (Python 3.10+)

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> None:
    if is_string_list(items):
        # items is now list[str]
        print(", ".join(items))
```

### TypeIs (Python 3.13+)

```python
from typing import TypeIs

def is_str(val: object) -> TypeIs[str]:
    return isinstance(val, str)

def process(val: int | str) -> None:
    if is_str(val):
        print(val.upper())  # val is str
    else:
        print(val + 1)  # val is int
```

## Literal Types

```python
from typing import Literal

Mode = Literal["r", "w", "a"]

def open_file(path: str, mode: Mode) -> None:
    ...

open_file("data.txt", "r")  # ✅
open_file("data.txt", "x")  # ❌ Error
```

## Final and ClassVar

```python
from typing import Final, ClassVar

class Config:
    # Class variable (not instance variable)
    instances: ClassVar[int] = 0
    
    # Cannot be reassigned
    VERSION: Final = "1.0.0"
    
    def __init__(self) -> None:
        Config.instances += 1
```

## Self Type (Python 3.11+)

```python
from typing import Self

class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self  # Returns same type, even in subclasses

class AdvancedBuilder(Builder):
    def set_extra(self, extra: str) -> Self:
        self.extra = extra
        return self

# Chaining works correctly
builder = AdvancedBuilder().set_name("test").set_extra("data")
```

## Annotated

```python
from typing import Annotated

# Add metadata to types (for validators, docs, etc.)
UserId = Annotated[int, "positive integer representing user ID"]
Email = Annotated[str, "valid email address"]

def get_user(user_id: UserId, email: Email) -> dict:
    ...
```

## Never and NoReturn

```python
from typing import Never, NoReturn

# Function that never returns normally
def fail(message: str) -> NoReturn:
    raise RuntimeError(message)

# Type that has no valid values (Python 3.11+)
def unreachable() -> Never:
    raise AssertionError("This should never be called")
```

## Type Narrowing

```python
def process(value: int | str | None) -> str:
    # isinstance narrows type
    if isinstance(value, str):
        return value.upper()  # value is str
    
    # None check narrows type
    if value is None:
        return "default"  # value is None
    
    # Remaining type
    return str(value)  # value is int
```

## Overloads

```python
from typing import overload

@overload
def parse(data: str) -> dict: ...
@overload
def parse(data: bytes) -> dict: ...
@overload
def parse(data: None) -> None: ...

def parse(data: str | bytes | None) -> dict | None:
    if data is None:
        return None
    if isinstance(data, bytes):
        data = data.decode()
    return {"parsed": data}
```

## Forward References

```python
from __future__ import annotations  # Enable postponed evaluation

class Node:
    # Can reference Node before it's fully defined
    def add_child(self, child: Node) -> None:
        ...

# Or use string literal
class Tree:
    def get_root(self) -> "Tree":
        ...
```

## Common Patterns

### Factory Function

```python
from typing import TypeVar, Type

T = TypeVar("T")

def create(cls: Type[T], **kwargs) -> T:
    return cls(**kwargs)
```

### Context Manager

```python
from typing import ContextManager
from contextlib import contextmanager

@contextmanager
def open_resource(name: str) -> ContextManager[Resource]:
    resource = Resource(name)
    try:
        yield resource
    finally:
        resource.close()
```

### Async Types

```python
from typing import AsyncIterator, Awaitable
from collections.abc import Coroutine

async def fetch() -> str:
    return "data"

async def stream() -> AsyncIterator[int]:
    for i in range(10):
        yield i

# Awaitable
task: Awaitable[str] = fetch()
```
