from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.base_class import Base

class ChatHistory(Base):
    """
    Model to store chat messages and AI responses.
    """
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    message = Column(String, nullable=False)
    is_user_message = Column(Boolean, default=True) # True: User, False: AI
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationship to User model
    user = relationship("User", back_populates="chats")