from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ProjectTag(str, Enum):
    """Tags to categorize different parts of the project"""
    SETUP = "setup"
    MVP = "mvp"
    FRONTEND = "frontend"
    BACKEND = "backend"
    AUTH = "auth"
    DATABASE = "database"
    DEPLOYMENT = "deployment"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DESIGN = "design"
    API = "api"
    INTEGRATION = "integration"
    OPTIMIZATION = "optimization"
    SECURITY = "security"

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
    phase: str = "discovery"  # discovery, confirmation, generation, editing
    specifications_complete: bool = False
    project_specification: Optional[ProjectSpecification] = None
    current_roadmap: Optional[Roadmap] = None
    messages: List[ChatMessage] = []