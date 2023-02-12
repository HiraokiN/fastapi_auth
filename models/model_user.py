from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    group=Column(Integer, index=True, nullable=False)
    name = Column(String, unique= True, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    git_info = relationship("GitInfo", back_populates="owner", uselist=False)
    stacks = relationship("Stack", back_populates="owner")