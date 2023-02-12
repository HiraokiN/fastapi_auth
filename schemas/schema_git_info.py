from typing import List, Union
from pydantic import BaseModel

class GitInfoBase(BaseModel):
    gitlab_token: str
    git_name: str
    git_email: str


class GitInfoCreate(GitInfoBase):
    pass


class GitInfo(GitInfoBase):
    id: int
    owener_id: int

    class Config:
        orm_mode = True
    