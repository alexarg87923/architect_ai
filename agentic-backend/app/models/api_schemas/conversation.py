from pydantic import BaseModel
from typing import List, Optional
from .roadmap import ProjectSpecification, Roadmap

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
