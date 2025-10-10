from .base import BASE
from sqlalchemy.types import Boolean, DateTime,UUID
from sqlalchemy.orm import mapped_column, Mapped,relationship
from sqlalchemy import text, func
from sqlalchemy.sql.schema import ForeignKey
from datetime import datetime
from uuid import uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users import Users



class RefreshTokens(BASE):
    __tablename__ = "refresh_tokens"

    id            : Mapped[str]   = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    user_id   : Mapped[str]      = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    jti       : Mapped[str]      = mapped_column(unique=True, nullable=False, default=uuid4)
    revoked   : Mapped[bool]     = mapped_column(Boolean, nullable=False, default=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user : Mapped["Users"] = relationship(back_populates="refresh_tokens")
