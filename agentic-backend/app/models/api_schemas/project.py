from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .roadmap import Roadmap
from .task import TasksByType

class ProjectBase(BaseModel):
    """Base project model with common fields"""
    name: str
    description: Optional[str] = None
    status: str = "draft"  # draft, active, completed, archived

class ProjectCreate(ProjectBase):
    """Model for creating a new project"""
    pass

class ProjectUpdate(BaseModel):
    """Model for updating a project"""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    roadmap_data: Optional[Roadmap] = None

class Project(ProjectBase):
    """Complete project model with ID and timestamps"""
    id: int
    user_id: int
    roadmap_data: Optional[Roadmap] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    """Project response model for API responses"""
    id: int
    name: str
    description: Optional[str] = None
    status: str
    roadmap_data: Optional[Roadmap] = None
    tasks: Optional[TasksByType] = None
    created_at: datetime
    updated_at: datetime
