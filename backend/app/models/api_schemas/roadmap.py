from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Story(BaseModel):
    """Individual story within an epic"""
    id: int
    title: str
    acceptance_criteria: List[str] = []
    completed: bool = False

class Epic(BaseModel):
    """High-level feature epic containing multiple stories"""
    id: int
    name: str
    priority: str  # P0, P1, P2
    description: str
    stories: List[Story] = []

class Project(BaseModel):
    """Project information"""
    name: str
    vision: str
    type: str
    target_users: str

class Architecture(BaseModel):
    """System architecture design"""
    mermaid_diagram: str
    components: List[str] = []

class Roadmap(BaseModel):
    """Complete project roadmap with epics and architecture"""
    project: Project
    epics: List[Epic]
    architecture: Architecture
    message: Optional[str] = None  # Confirmation message to display to user

# Backward compatibility aliases (for existing code that uses old names)
SubTask = Story
RoadmapNode = Epic
ProjectSpecification = Project

class UpdateEpic(BaseModel):
    """Request model for updating existing epics"""
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    stories: Optional[List[Story]] = None
    priority: Optional[str] = None

class ExpandEpicRequest(BaseModel):
    """Request to expand an epic with additional stories/details"""
    epic_id: int
    expansion_details: str
    context: Optional[str] = None
