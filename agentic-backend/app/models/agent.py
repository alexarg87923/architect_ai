from pydantic import BaseModel, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import datetime

# User Models
class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True

class UserCreate(UserBase):
    """Model for creating a new user"""
    password: Optional[str] = None  # Optional for dev dummy user

class User(UserBase):
    """Complete user model with ID and timestamps"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """User response model for API responses"""
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool

class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr

class LoginResponse(BaseModel):
    """Login response model"""
    user: UserResponse
    message: str

class ProjectTag(str, Enum):
    """Tags to categorize different parts of student personal projects"""
    SETUP = "setup"
    MVP = "mvp"
    FRONTEND = "frontend"
    BACKEND = "backend"
    AUTH = "auth"
    DEPLOYMENT = "deployment"
    TESTING = "testing"

class SubTask(BaseModel):
    """Individual subtask within a roadmap node"""
    id: str
    title: str
    description: str
    completed: bool = False
    estimated_hours: Optional[float] = None

class RoadmapNode(BaseModel):
    """Actionable project milestone with clear deliverables"""
    id: str
    title: str
    description: str
    
    # Actionable subtasks
    subtasks: List[SubTask] = []
    
    # Timeline estimates
    estimated_days: int  # How many days to complete
    estimated_hours: float  # Total work hours needed
    
    # Project categorization
    tags: List[ProjectTag] = []
    
    # Dependencies and relationships
    dependencies: List[str] = []  # IDs of nodes that must be completed first
    
    # Progress tracking
    status: str = "pending"  # pending, in_progress, completed
    completion_percentage: int = 0
    
    # Additional context
    deliverables: List[str] = []  # What the user should have after completing this node
    success_criteria: List[str] = []  # How to know the node is truly complete
    
    # Project overview (for setup nodes)
    overview: Optional[List[str]] = None  # High-level development strategy steps

class ProjectSpecification(BaseModel):
    """Complete project specifications gathered from user conversation"""
    title: str
    description: str
    goals: List[str]
    timeline_weeks: Optional[int] = None
    tech_stack: List[str] = []
    user_experience_level: str = "beginner"  # beginner, intermediate, advanced
    deployment_needed: bool = False
    auth_needed: bool = False
    commercialization_goal: bool = False
    target_audience: str = ""
    similar_projects_built: bool = False

class Roadmap(BaseModel):
    """Complete project roadmap with all nodes and specifications"""
    project_specification: ProjectSpecification
    nodes: List[RoadmapNode]
    total_estimated_weeks: Optional[int] = None
    total_estimated_hours: Optional[float] = None

# Project Models
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
    created_at: datetime
    updated_at: datetime

class UpdateNode(BaseModel):
    """Request model for updating existing nodes"""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    subtasks: Optional[List[SubTask]] = None
    estimated_days: Optional[int] = None
    estimated_hours: Optional[float] = None
    tags: Optional[List[ProjectTag]] = None
    dependencies: Optional[List[str]] = None
    deliverables: Optional[List[str]] = None
    success_criteria: Optional[List[str]] = None

class ExpandNodeRequest(BaseModel):
    """Request to expand a node with additional subtasks/details"""
    node_id: str
    expansion_details: str
    context: Optional[str] = None

class ChatMessage(BaseModel):
    """Chat message between user and agent"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[str] = None
    action_type: Optional[str] = None  # "chat", "generate_roadmap", "expand_node", "edit_node"

class ConversationState(BaseModel):
    """Current state of the conversation with the agent"""
    session_id: str
    user_id: Optional[int] = None  # Associate conversation with user
    phase: str = "discovery"  # discovery, confirmation, generation, subtask_generation, editing
    specifications_complete: bool = False
    project_specification: Optional[ProjectSpecification] = None
    current_roadmap: Optional[Roadmap] = None
    messages: List[ChatMessage] = []
    nodes_needing_subtasks: List[str] = []  # Track which nodes still need subtasks