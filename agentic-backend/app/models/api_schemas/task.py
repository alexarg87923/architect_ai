from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    """Base task model with common fields"""
    text: str
    completed: bool = False
    task_type: str  # "daily-todos" or "your-ideas"

class TaskCreate(TaskBase):
    """Model for creating a new task"""
    pass

class TaskUpdate(BaseModel):
    """Model for updating a task"""
    text: Optional[str] = None
    completed: Optional[bool] = None
    task_type: Optional[str] = None
    archive: Optional[bool] = None

class Task(TaskBase):
    """Complete task model with ID and timestamps"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    """Task response model for API responses"""
    id: int
    project_id: int
    text: str
    completed: bool
    task_type: str
    created_at: datetime
    updated_at: datetime
    archive: Optional[bool] = False

class TasksByType(BaseModel):
    """Model for grouping tasks by type"""
    daily_todos: List[TaskResponse] = []
    your_ideas: List[TaskResponse] = []
