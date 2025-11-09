# Service registry - centralized service instances
from .user_service import UserService
from .project_service import ProjectService
from .task_service import TaskService
from .feedback_service import FeedbackService
from .database_service import DatabaseService
from .agent_service import AgentService

# Create singleton instances
user_service = UserService()
project_service = ProjectService()
task_service = TaskService()
feedback_service = FeedbackService()
database_service = DatabaseService()
agent_service = AgentService()

__all__ = [
    "user_service",
    "project_service", 
    "task_service",
    "feedback_service",
    "database_service",
    "agent_service"
]