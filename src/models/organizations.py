from sqlalchemy import UUID
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql.schema import ForeignKey
from datetime import date
from typing import TYPE_CHECKING

from .base import BASE

if TYPE_CHECKING:
    from .buildings import Buildings
    from .activities import Activities



class Organizations(BASE):
    __tablename__ = "organizations"

    id            : Mapped[str]   = mapped_column(UUID(as_uuid=True), primary_key=True)
    building_id   : Mapped[str]   = mapped_column(ForeignKey("buildings.id"), nullable=False)
    activity_id   : Mapped[str]   = mapped_column(ForeignKey("activities.id"),nullable=False)
    latitude      : Mapped[float] = mapped_column(nullable=False)
    longitude     : Mapped[float] = mapped_column(nullable=False)
    created_at    : Mapped[date]  = mapped_column(nullable=False)

    building      : Mapped["Buildings"]  = relationship(back_populates="organizations")
    activity      : Mapped["Activities"] = relationship(back_populates="organizations")