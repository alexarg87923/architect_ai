from sqlalchemy import Column, Integer, Text, DateTime, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    task_type = Column(String, nullable=False)  # "daily-todos" or "your-ideas"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archive = Column(Boolean, default=False)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
