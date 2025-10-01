from pydantic import BaseModel,Field
from uuid import UUID
from typing import Optional

class Building(BaseModel):
    pass


class SelectBuilding(BaseModel):
    id: Optional[UUID] = None  
    name          : str 
    latitude      : float 
    longitude     : float 


class AddBuilding(BaseModel):
    name          : str   = Field(min_length=2,max_length=50)
    latitude      : float = Field(ge=-90,le=90)
    longitude     : float = Field(ge=-180,le=180)
