from sqlalchemy import UUID, TEXT
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING

from .base import BASE

from uuid import uuid4
if TYPE_CHECKING:
    from .organizations import Organizations

class Activities(BASE):
    __tablename__ = "activities"

    id           : Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid4)
    name         : Mapped[str] = mapped_column(TEXT, nullable=False)

    organizations: Mapped[list["Organizations"]] = relationship(back_populates="activity")
