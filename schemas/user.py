from typing import List, Union
from pydantic import BaseModel
from .stack import Stack

class UserBase(BaseModel):
    name: str
    hashed_password: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    stacks: List[Stack]  = []
    git_info_id: int

    class Config:
        orm_mode = True
    