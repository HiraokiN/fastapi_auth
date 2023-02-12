from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Stack(Base):
    __tablename__ = "stack"
    id = Column(Integer, primary_key=True, index=True)
    stack_id = Column(Integer, index=True)
    stack_name = Column(String)
    port = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="stacks",)