from pydantic import BaseModel,Field,field_validator,EmailStr
import re
from datetime import datetime,date,timezone
from uuid import UUID
from typing import Optional


class User(BaseModel):
    pass

class UserInfo(User):
    id              :   UUID = None  
    name            :   str       = Field(min_length=2,max_length=50)
    email           :   EmailStr  = Field(min_length=5,max_length=50)


class AddUser(UserInfo):
    password        : str       = Field(min_length=5,max_length=50)
    created_at      : date      = Field(default=date.today())
    organizations_id: UUID       

class UserAuthentication(User):
    name    : str = Field(min_length=2,max_length=50)
    password: str = Field(min_length=5,max_length=50)
    

class AddTokenToUser(BaseModel):
    user_id   : UUID
    jti       : str
    expires_at: datetime
    revoked   : bool
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


