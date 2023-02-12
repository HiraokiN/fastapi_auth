from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class GitInfo(Base):
    __tablename__ = "git_info"
    id = Column(Integer, primary_key=True, index=True)
    gitlab_token = Column(String, index=True, default="")
    git_name = Column(String, default="")
    git_email = Column(String, default="")
    owner_id = Column(Integer, ForeignKey("users.id"), unique=True)

    owner = relationship("User", back_populates="git_info")
