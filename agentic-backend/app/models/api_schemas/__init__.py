# API schemas package - Pydantic models for request/response validation
from .user import UserBase, UserCreate, UserUpdate, User, UserResponse, LoginRequest, LoginResponse, ChangePasswordRequest, ChangePasswordResponse
from .project import ProjectBase, ProjectCreate, ProjectUpdate, Project, ProjectResponse
from .task import TaskBase, TaskCreate, TaskUpdate, Task, TaskResponse, TasksByType
from .conversation import ConversationState, ChatMessage
from .roadmap import Roadmap, RoadmapNode, SubTask, ProjectSpecification, UpdateNode, ExpandNodeRequest, ProjectTag
from .feedback import FeedbackBase, FeedbackCreate, FeedbackUpdate, Feedback, FeedbackResponse

__all__ = [
    # User schemas
    "UserBase", "UserCreate", "UserUpdate", "User", "UserResponse", 
    "LoginRequest", "LoginResponse", "ChangePasswordRequest", "ChangePasswordResponse",
    # Project schemas
    "ProjectBase", "ProjectCreate", "ProjectUpdate", "Project", "ProjectResponse",
    # Task schemas
    "TaskBase", "TaskCreate", "TaskUpdate", "Task", "TaskResponse", "TasksByType",
    # Conversation schemas
    "ConversationState", "ChatMessage",
    # Roadmap schemas
    "Roadmap", "RoadmapNode", "SubTask", "ProjectSpecification", "UpdateNode", "ExpandNodeRequest", "ProjectTag",
    # Feedback schemas
    "FeedbackBase", "FeedbackCreate", "FeedbackUpdate", "Feedback", "FeedbackResponse"
]
