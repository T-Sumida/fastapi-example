from pydantic import BaseModel, EmailStr
from typing import Optional


class BaseUser(BaseModel):
    email: EmailStr
    last_name: str
    first_name: str
    is_admin: bool
    

class CreateUser(BaseUser):
    password: str
    

class UpdateUser(BaseUser):
    password: Optional[str]
    last_name: Optional[str]
    first_name: Optional[str]
    is_admin: bool
    

class UserInDB(BaseUser):
    class Config:
        orm_mode = True