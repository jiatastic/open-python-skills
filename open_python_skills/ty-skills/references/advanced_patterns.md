# Advanced Type Patterns

Advanced typing patterns for complex Python codebases.

## Intersection Types (ty Exclusive)

ty has first-class support for intersection types, which represent values that satisfy multiple type constraints simultaneously.

### Basic Intersection

```python
def output_as_json(obj: Serializable) -> str:
    if isinstance(obj, Versioned):
        reveal_type(obj)  # reveals: Serializable & Versioned
        
        # Can access members from BOTH types
        return str({
            "data": obj.serialize_json(),  # From Serializable
            "version": obj.version          # From Versioned
        })
    return obj.serialize_json()
```

### Intersection with hasattr

```python
class Person:
    name: str

class Animal:
    species: str

def greet(being: Person | Animal | None):
    if hasattr(being, "name"):
        # Type: Person | (Animal & <Protocol with 'name'>)
        print(f"Hello, {being.name}!")
    else:
        print("Hello there!")
```

### Explicit Intersection Type

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ty_extensions import Intersection
    
    type SerializableVersioned = Intersection[Serializable, Versioned]

def output_as_json(obj: SerializableVersioned) -> str:
    # Can directly access both interfaces
    return str({
        "data": obj.serialize_json(),
        "version": obj.version
    })
```

---

## Protocol Patterns

### Basic Protocol

```python
from typing import Protocol

class Comparable(Protocol):
    def __lt__(self, other: object) -> bool: ...
    def __eq__(self, other: object) -> bool: ...

def find_min(items: list[Comparable]) -> Comparable:
    return min(items)

# Works with any class implementing __lt__ and __eq__
find_min([3, 1, 2])  # ✅ int has these methods
find_min(["c", "a", "b"])  # ✅ str has these methods
```

### Protocol with Properties

```python
from typing import Protocol

class Named(Protocol):
    @property
    def name(self) -> str: ...

class Identifiable(Protocol):
    @property
    def id(self) -> int: ...
    
    @property
    def name(self) -> str: ...

def display(item: Named) -> None:
    print(item.name)
```

### Generic Protocol

```python
from typing import Protocol, TypeVar

T_co = TypeVar("T_co", covariant=True)

class Container(Protocol[T_co]):
    def get(self) -> T_co: ...

class Box:
    def __init__(self, value: int) -> None:
        self._value = value
    
    def get(self) -> int:
        return self._value

def extract(container: Container[int]) -> int:
    return container.get()

extract(Box(42))  # ✅ Works
```

### Callback Protocol

```python
from typing import Protocol

class EventHandler(Protocol):
    def __call__(self, event: str, data: dict) -> None: ...

def register_handler(handler: EventHandler) -> None:
    handler("startup", {})

# Lambda works
register_handler(lambda event, data: print(event))

# Function works
def my_handler(event: str, data: dict) -> None:
    print(f"{event}: {data}")

register_handler(my_handler)

# Class with __call__ works
class LogHandler:
    def __call__(self, event: str, data: dict) -> None:
        print(f"[LOG] {event}")

register_handler(LogHandler())
```

---

## Variance

### Covariance (Output Positions)

```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)

class Producer(Generic[T_co]):
    def get(self) -> T_co: ...

# Producer[Dog] is subtype of Producer[Animal]
# Because if you can produce Dogs, you can produce Animals

class Animal: pass
class Dog(Animal): pass

def use_producer(p: Producer[Animal]) -> Animal:
    return p.get()

dog_producer: Producer[Dog] = ...
use_producer(dog_producer)  # ✅ Covariance allows this
```

### Contravariance (Input Positions)

```python
from typing import TypeVar, Generic

T_contra = TypeVar("T_contra", contravariant=True)

class Consumer(Generic[T_contra]):
    def accept(self, item: T_contra) -> None: ...

# Consumer[Animal] is subtype of Consumer[Dog]
# Because if you can consume any Animal, you can certainly consume Dogs

def use_consumer(c: Consumer[Dog]) -> None:
    c.accept(Dog())

animal_consumer: Consumer[Animal] = ...
use_consumer(animal_consumer)  # ✅ Contravariance allows this
```

### Invariance (Both Positions)

```python
from typing import TypeVar, Generic

T = TypeVar("T")  # Invariant by default

class MutableContainer(Generic[T]):
    def get(self) -> T: ...
    def set(self, value: T) -> None: ...

# MutableContainer[Dog] is NOT related to MutableContainer[Animal]
# Because you could put a Cat into a MutableContainer[Animal]
```

---

## Type Guard Patterns

### Basic TypeGuard

```python
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    """Narrow list[object] to list[str]."""
    return all(isinstance(x, str) for x in val)

def process(items: list[object]) -> str:
    if is_string_list(items):
        # items is now list[str]
        return ", ".join(items)
    return str(items)
```

### TypeGuard with Union

```python
from typing import TypeGuard

class Success:
    value: str

class Error:
    message: str

type Result = Success | Error

def is_success(result: Result) -> TypeGuard[Success]:
    return isinstance(result, Success)

def handle(result: Result) -> str:
    if is_success(result):
        return result.value  # result is Success
    return f"Error: {result.message}"  # result is Error
```

### TypeIs (Python 3.13+)

```python
from typing import TypeIs

def is_str(val: str | int) -> TypeIs[str]:
    return isinstance(val, str)

def process(val: str | int) -> None:
    if is_str(val):
        print(val.upper())  # val is str
    else:
        print(val + 1)  # val is int (properly narrowed)
```

---

## Decorator Patterns

### Preserving Signatures with ParamSpec

```python
from typing import TypeVar, ParamSpec, Callable
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def with_retry(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        for attempt in range(3):
            try:
                return func(*args, **kwargs)
            except Exception:
                if attempt == 2:
                    raise
        raise RuntimeError("Unreachable")
    return wrapper

@with_retry
def fetch_data(url: str, timeout: int = 30) -> dict:
    ...

# Type signature preserved!
fetch_data("https://api.example.com", timeout=60)
```

### Decorator that Changes Return Type

```python
from typing import TypeVar, ParamSpec, Callable, Awaitable
from functools import wraps

P = ParamSpec("P")
R = TypeVar("R")

def make_async(func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)
    return wrapper

@make_async
def compute(x: int, y: int) -> int:
    return x + y

# Now returns Awaitable[int]
result = await compute(1, 2)
```

### Class Decorator

```python
from typing import TypeVar, Type

T = TypeVar("T")

def singleton(cls: Type[T]) -> Type[T]:
    instances: dict[Type[T], T] = {}
    
    original_new = cls.__new__
    
    def new_new(cls: Type[T], *args, **kwargs) -> T:
        if cls not in instances:
            instances[cls] = original_new(cls)
        return instances[cls]
    
    cls.__new__ = new_new  # type: ignore
    return cls

@singleton
class Database:
    def __init__(self) -> None:
        self.connected = False
```

---

## Factory Patterns

### Generic Factory

```python
from typing import TypeVar, Type

T = TypeVar("T")

def create(cls: Type[T], **kwargs) -> T:
    return cls(**kwargs)

class User:
    def __init__(self, name: str, email: str) -> None:
        self.name = name
        self.email = email

user = create(User, name="Alice", email="alice@example.com")
reveal_type(user)  # User
```

### Abstract Factory with Protocol

```python
from typing import Protocol, TypeVar

class Connection(Protocol):
    def execute(self, query: str) -> list: ...

class ConnectionFactory(Protocol):
    def create(self) -> Connection: ...

def run_query(factory: ConnectionFactory, query: str) -> list:
    conn = factory.create()
    return conn.execute(query)
```

---

## Recursive Types

### Self-Referential Type

```python
from __future__ import annotations

class TreeNode:
    def __init__(self, value: int) -> None:
        self.value = value
        self.children: list[TreeNode] = []
    
    def add_child(self, child: TreeNode) -> TreeNode:
        self.children.append(child)
        return self
```

### Recursive Type Alias

```python
from typing import Union

# JSON type
type JSON = dict[str, JSON] | list[JSON] | str | int | float | bool | None

def parse_json(data: str) -> JSON:
    import json
    return json.loads(data)
```

---

## Overload Patterns

### Return Type Based on Input

```python
from typing import overload, Literal

@overload
def fetch(url: str, raw: Literal[True]) -> bytes: ...
@overload
def fetch(url: str, raw: Literal[False] = ...) -> str: ...

def fetch(url: str, raw: bool = False) -> bytes | str:
    data = _download(url)
    return data if raw else data.decode()

# Type-safe usage
text: str = fetch("https://example.com")
binary: bytes = fetch("https://example.com", raw=True)
```

### Overload with Optional

```python
from typing import overload

@overload
def get_user(id: int) -> User: ...
@overload
def get_user(id: None) -> None: ...

def get_user(id: int | None) -> User | None:
    if id is None:
        return None
    return User.fetch(id)

# Precise return types
user: User = get_user(42)
nothing: None = get_user(None)
```

---

## Context Manager Typing

```python
from typing import Generator
from contextlib import contextmanager

@contextmanager
def managed_resource(name: str) -> Generator[Resource, None, None]:
    resource = Resource(name)
    try:
        yield resource
    finally:
        resource.close()

# Async context manager
from typing import AsyncGenerator
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_session() -> AsyncGenerator[Session, None]:
    session = await Session.create()
    try:
        yield session
    finally:
        await session.close()
```
