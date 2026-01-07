# Database Patterns

SQLAlchemy and Alembic patterns for Python backends.

## Async Engine + Session

Use async engine + async session per request:

```python
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/app"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
```

---

## Commit/Rollback Pattern

Wrap write operations in try/except:

```python
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, user: dict) -> User:
    try:
        db_user = User(**user)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    except Exception:
        await session.rollback()
        raise
```

### Nested Transaction with Savepoint

```python
async def transfer_funds(session: AsyncSession, from_id: int, to_id: int, amount: float):
    async with session.begin_nested():  # Creates a savepoint
        from_account = await session.get(Account, from_id)
        to_account = await session.get(Account, to_id)
        
        if from_account.balance < amount:
            raise InsufficientFunds()
        
        from_account.balance -= amount
        to_account.balance += amount
    
    await session.commit()
```

---

## Naming Conventions

Be consistent with names:
1. lower_case_snake
2. singular form (e.g. post, post_like, user_playlist)
3. group similar tables with module prefix (e.g. payment_account, payment_bill)
4. stay consistent across tables
5. _at suffix for datetime, _date suffix for date

### Constraint Naming

```python
from sqlalchemy import MetaData

NAMING_CONVENTION = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

metadata = MetaData(naming_convention=NAMING_CONVENTION)
```

---

## Alembic Migration Naming

Use human-readable file template:

```ini
# alembic.ini
file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(slug)s
# Results in: 2024-08-24_add_users_table.py
```

---

## Eager Loading - Avoid N+1

### selectinload for collections

```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

# Load all users with their orders in 2 queries
stmt = select(User).options(selectinload(User.orders))
users = await session.scalars(stmt)

for user in users:
    print(user.orders)  # No additional query
```

### joinedload for single relationships

```python
from sqlalchemy.orm import joinedload

# Load orders with their user in 1 query (JOIN)
stmt = select(Order).options(joinedload(Order.user))
orders = await session.scalars(stmt)
```

### raiseload to detect N+1

```python
from sqlalchemy.orm import raiseload

stmt = select(User).options(
    selectinload(User.orders),
    raiseload("*")  # Raise on any other lazy load
)
```

---

## Cascade Delete

Configure at both ORM and database level:

```python
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Parent(Base):
    __tablename__ = "parent"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    children: Mapped[list["Child"]] = relationship(
        back_populates="parent",
        cascade="all, delete",
        passive_deletes=True,
    )

class Child(Base):
    __tablename__ = "child"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("parent.id", ondelete="CASCADE")
    )
    
    parent: Mapped["Parent"] = relationship(back_populates="children")
```

---

## Soft Delete Pattern

Use a deleted_at timestamp instead of hard deletes:

```python
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property

class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), 
        default=None,
        index=True
    )
    
    @hybrid_property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None
    
    def soft_delete(self) -> None:
        self.deleted_at = datetime.utcnow()
    
    def restore(self) -> None:
        self.deleted_at = None
```

Filter soft-deleted:

```python
# Only get non-deleted users
stmt = select(User).where(User.deleted_at.is_(None))

# Only deleted
stmt_deleted = select(User).where(User.deleted_at.isnot(None))
```

---

## Optimistic Locking

Use version_id_col to prevent lost updates:

```python
class Article(Base):
    __tablename__ = "article"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    version_id: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    
    __mapper_args__ = {
        "version_id_col": version_id
    }

# Handle StaleDataError
from sqlalchemy.orm.exc import StaleDataError

async def update_article(session: AsyncSession, article_id: int, data: dict):
    try:
        article = await session.get(Article, article_id)
        for key, value in data.items():
            setattr(article, key, value)
        await session.commit()
    except StaleDataError:
        await session.rollback()
        raise ConcurrentModificationError("Article was modified by another user.")
```

---

## Timestamp Mixin

Automatic created_at and updated_at:

```python
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
```

---

## Bulk Operations

### Bulk Insert

```python
from sqlalchemy import insert

async def bulk_create_users(session: AsyncSession, users: list[dict]):
    await session.execute(
        insert(User),
        [
            {"name": "Alice", "email": "alice@example.com"},
            {"name": "Bob", "email": "bob@example.com"},
        ],
    )
    await session.commit()
```

### Bulk Update

```python
from sqlalchemy import update

async def deactivate_old_users(session: AsyncSession, days: int = 365):
    from datetime import datetime, timedelta
    
    cutoff = datetime.utcnow() - timedelta(days=days)
    
    result = await session.execute(
        update(User)
        .where(User.last_login < cutoff)
        .values(is_active=False)
    )
    await session.commit()
    
    return result.rowcount
```

---

## Upsert (PostgreSQL)

```python
from sqlalchemy.dialects.postgresql import insert as pg_insert

async def upsert_user(session: AsyncSession, user_data: dict):
    stmt = pg_insert(User).values(**user_data)
    
    stmt = stmt.on_conflict_do_update(
        index_elements=[User.email],
        set_={
            "name": stmt.excluded.name,
            "updated_at": func.now(),
        }
    )
    
    await session.execute(stmt)
    await session.commit()
```

---

## UUID Primary Keys

```python
import uuid
from sqlalchemy import Uuid
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user"
    
    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid4
    )
```

### Dual ID Pattern (internal + public)

```python
class User(Base):
    __tablename__ = "user"
    
    # Internal ID for joins (faster)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    # Public ID for API (safe to expose)
    public_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        unique=True,
        default=uuid.uuid4,
        index=True
    )
```

---

## Repository Pattern

```python
from typing import Generic, TypeVar, Type
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model
    
    async def get(self, id: int) -> ModelType | None:
        return await self.session.get(self.model, id)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = await self.session.scalars(
            select(self.model).offset(skip).limit(limit)
        )
        return result.all()
    
    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.scalar(
            select(User).where(User.email == email)
        )
        return result
```
