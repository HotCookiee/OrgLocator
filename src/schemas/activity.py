from pydantic import BaseModel, ConfigDict, Field, field_validator
from uuid import UUID
from typing import Optional


class Activity(BaseModel):
    pass


class SelectActivity(Activity):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[UUID] = None
    name: str


class AddActivity(Activity):
    name: str = Field(min_length=2, max_length=50)
