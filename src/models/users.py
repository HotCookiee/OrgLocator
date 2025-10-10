from sqlalchemy import UUID, TEXT
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKey
from datetime import date
from typing import TYPE_CHECKING


from .base import BASE

from uuid import uuid4

if TYPE_CHECKING:
    from .organizations import Organizations
    from .refresh_tokens import RefreshTokens




class Users(BASE):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[date] = mapped_column(nullable=False, default=date.today())
    organizations_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id")
    )

    refresh_tokens: Mapped[list["RefreshTokens"]] = relationship(back_populates="user",cascade="all, delete-orphan",passive_deletes=True)
    organizations: Mapped["Organizations"] = relationship(back_populates="users")
    
