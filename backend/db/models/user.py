from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from backend.db.base_class import Base

class User(Base):
    """
    Database model for Application Users.
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relationship with ChatHistory model
    # 'back_populates' must match the relationship name in chat.py
    chats = relationship("ChatHistory", back_populates="user")