from pydantic import BaseModel,Field
from datetime import date


class Organization(BaseModel):
    id            : str   
    building_id   : str   
    activity_id   : str   
    latitude      : float 
    longitude     : float 
    created_at    : date  
