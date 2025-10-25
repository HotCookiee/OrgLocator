from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from uuid import UUID
from typing import Optional


class Organization(BaseModel):
    
    pass


class SelectOrganization(Organization):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = None
    name: str
    building_id: str | UUID
    activity_id: str | UUID
    created_at: date = Field()


class AddOrganization(Organization):
    building_id: str
    activity_id: str
    created_at: date
    name: str
