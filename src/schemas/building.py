from pydantic import BaseModel,Field


class Building(BaseModel):
    id            : str  
    name          : str 
    latitude      : float 
    longitude     : float 