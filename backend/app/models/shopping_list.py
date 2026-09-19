import secrets
from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Index,
    String,
    Uuid,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User


def generate_share_token() -> str:
    return secrets.token_urlsafe(32)


class ShoppingList(Base):
    __tablename__ = "shopping_lists"
    __table_args__ = (
        Index(
            "uq_shopping_lists_owner_active",
            "owner_id",
            unique=True,
            sqlite_where=text("completed_at IS NULL"),
            postgresql_where=text("completed_at IS NULL"),
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    owner_id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    share_token: Mapped[str] = mapped_column(
        String(64),
        default=generate_share_token,
        unique=True,
        index=True,
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    owner: Mapped["User"] = relationship(
        back_populates="shopping_lists",
    )
