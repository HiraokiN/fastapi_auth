from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique= True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    git_info = relationship("GitInfo", back_populates="owner")
    stacks = relationship("Stack", back_populates="owner")

class GitInfo(Base):
    __tablename__ = "git_info"
    id = Column(Integer, primary_key=True, index=True)
    gitlab_token = Column(String, index=True, default="")
    git_name = Column(String, default="")
    git_email = Column(String, default="")
    owner = relationship("User", back_populates="git_info")

class Stack(Base):
    __tablename_ = "Stack"
    id = Column(Integer, primary_key=True, index=True)
    stack_id = Column(Integer, index=True)
    stack_name = Column(String)
    port = Column(Integer)
    owner = relationship("User", back_populates="stacks")