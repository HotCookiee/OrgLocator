from sqlalchemy import UUID, TEXT,FLOAT
from sqlalchemy.orm import relationship, mapped_column, Mapped
from typing import TYPE_CHECKING

from .base import BASE

if TYPE_CHECKING:
    from .organizations import Organizations


class Buildings(BASE):
    __tablename__ = "buildings"

    id            : Mapped[str]   = mapped_column(UUID(as_uuid=True), primary_key=True)
    name          : Mapped[str]   = mapped_column(TEXT, nullable=False)
    latitude      : Mapped[float] = mapped_column(FLOAT, nullable=False)
    longitude     : Mapped[float] = mapped_column(FLOAT, nullable=False)

    organizations : Mapped[list["Organizations"]] = relationship(back_populates="building")