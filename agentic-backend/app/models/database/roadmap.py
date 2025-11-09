from sqlalchemy import Column, Integer, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Direct user association
    roadmap_data = Column(JSON)  # Store the full roadmap JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
    conversation = relationship("Conversation", back_populates="roadmaps")
