from typing import List, Union
from pydantic import BaseModel

class StackBase(BaseModel):
    stack_id: str
    stack_name: str
    port: str


class StackCreate(StackBase):
    pass


class Stack(StackBase):
    id: int
    owener_id: int

    class Config:
        orm_mode = True