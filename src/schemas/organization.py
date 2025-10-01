from pydantic import BaseModel,Field
from datetime import date
from uuid import UUID
from typing import Optional


class Organization(BaseModel):
    pass

class SelectOrganization(Organization):
    id: Optional[UUID] = None  
    building_id   : str   
    activity_id   : str   
    latitude      : float 
    longitude     : float 
    created_at    : date    


class AddOrganization(Organization):
    building_id   : str   
    activity_id   : str   
    latitude      : float 
    longitude     : float 
    created_at    : date  