# SKILL: Backend Engineer — FastAPI
## Domain: Python FastAPI Microservices

**Activation triggers:** new API endpoint, service layer method, SQLAlchemy
model, Pydantic schema, dependency injection, background task, middleware.

---

## FastAPI Endpoint Template

```python
from __future__ import annotations
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User

router = APIRouter()


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    value: Optional[float] = None


class ItemOut(BaseModel):
    id: str
    name: str
    value: Optional[float]
    created_at: str

    model_config = {"from_attributes": True}


@router.get("", response_model=List[ItemOut])
async def list_items(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> List[ItemOut]:
    """List all items owned by the current user."""
    # Implementation here
    ...


@router.post("", response_model=ItemOut, status_code=status.HTTP_201_CREATED)
async def create_item(
    body: ItemCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_active_user),
) -> ItemOut:
    """Create a new item."""
    # Implementation here
    ...
```

---

## SQLAlchemy Model Template

```python
import uuid
from datetime import datetime
from typing import Optional, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class MyModel(Base):
    __tablename__ = "my_table"
    __table_args__ = {"schema": "my_schema"}

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("iam.users.id", ondelete="CASCADE"),  # ALWAYS declare FK
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships — ForeignKey MUST be declared first (above)
    user: Mapped["User"] = relationship("User", back_populates="my_models", lazy="noload")
```

---

## Exception Handling Rules

```python
# CORRECT: catch specific types
@router.post("/oauth/google", response_model=AuthResponse)
async def google_oauth_login(data: OAuthCodeRequest, db: AsyncSession = Depends(get_db)):
    try:
        oauth_info = await OAuthService.get_google_user_info(code=data.code)
    except httpx.TimeoutException:
        raise HTTPException(503, "Google OAuth timed out — try again")
    except httpx.ConnectError:
        raise HTTPException(503, "Cannot reach Google OAuth servers")
    except ValueError as e:
        raise HTTPException(400, f"OAuth failed: {e}")

    # Code after try/except can also raise — FastAPI catches with its 500 handler
    user = await auth.create_oauth_user(oauth_info.model_dump())
    ...

# WRONG: catches too broadly and hides bugs
try:
    ...
except Exception:
    raise HTTPException(500, "Something went wrong")
```

---

## Global Exception Handler (add to every main.py)

```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url.path)},
    )
```

---

## SQLAlchemy Registry Collision Prevention

```python
# CHECK BEFORE NAMING: does any other model in the registry use this name?
# Pattern: prefix with domain when collision risk exists
class CopySubscription(Base):    # NOT "Subscription" — conflicts with iam.Subscription
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "copy_trading"}

class UserSubscription(Base):    # billing subscription
    __tablename__ = "subscriptions"
    __table_args__ = {"schema": "iam"}
```

---

## Async Query Patterns

```python
# List with pagination
from sqlalchemy import select

result = await db.execute(
    select(MyModel)
    .where(MyModel.user_id == user.id, MyModel.is_active.is_(True))
    .options(selectinload(MyModel.related))   # avoid N+1
    .order_by(MyModel.created_at.desc())
    .limit(limit)
    .offset(offset)
)
items = result.scalars().all()

# Raw SQL (use for complex queries)
result = await db.execute(
    text("SELECT id::text, name FROM my_schema.my_table WHERE user_id = :uid"),
    {"uid": str(user.id)},
)
rows = [dict(r) for r in result.mappings()]
```

---

## Anti-Patterns

```
✗ async def func() + blocking DB calls (use async SQLAlchemy only)
✗ Missing ForeignKey on relationship column
✗ Duplicate SQLAlchemy class names in registry
✗ Business logic in route handler (put in service layer)
✗ Missing await on DB commits
✗ Catching Exception without logging
✗ Returning raw SQLAlchemy objects without model validation
```
