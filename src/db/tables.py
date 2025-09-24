from sqlalchemy.orm import DeclarativeBase,relationship,mapped_column,Mapped
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy import UUID,TEXT,FLOAT
from datetime import date


class BASE (DeclarativeBase):
    pass




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


    



class Buildings(BASE):
    __tablename__ = "buildings"

    id            : Mapped[str]   = mapped_column(UUID(as_uuid=True), primary_key=True)
    name          : Mapped[str]   = mapped_column(TEXT, nullable=False)
    latitude      : Mapped[float] = mapped_column(FLOAT, nullable=False)
    longitude     : Mapped[float] = mapped_column(FLOAT, nullable=False)

    organizations : Mapped[list["Organizations"]] = relationship(back_populates="building")
 

class Activities(BASE):
    __tablename__ = "activities"

    id           : Mapped[str] = mapped_column(UUID(as_uuid=True), primary_key=True,nullable=False)
    name         : Mapped[str] = mapped_column(TEXT, nullable=False)

    organizations: Mapped[list["Organizations"]] = relationship(back_populates="activity")
    
    