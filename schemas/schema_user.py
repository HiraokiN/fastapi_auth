from typing import List, Union
from pydantic import BaseModel
from .schema_stack import Stack

class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str
    pass

class UserResponse(UserBase):
    group: int
    is_active: bool

class User(UserBase):
    password: str
    id: int
    group: int
    is_active: bool
    stacks: List[Stack]  = []
    git_info_id: int

    class Config:
        orm_mode = True
    