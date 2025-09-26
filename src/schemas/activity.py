from pydantic import BaseModel,Field,field_validator


class Activity(BaseModel):
    id : int
    name : str