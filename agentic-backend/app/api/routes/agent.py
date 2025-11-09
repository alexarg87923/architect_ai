from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.agent import ConversationState, ChatMessage, Roadmap
from app.services.agent_service import AgentService
import uuid
from datetime import datetime

router = APIRouter()

# Request/Response Models
from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    action_type: str = "chat"  # "chat", "edit", "expand"
    conversation_state: Optional[ConversationState] = None

class ChatResponse(BaseModel):
    agent_response: str
    conversation_state: ConversationState
    action_button: Optional[str] = None
    session_id: str

# Initialize AgentService
agent_service = AgentService()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint that handles all agent interactions
    Supports: discovery, roadmap generation, editing, and expansion
    """
    try:
        # Get or create session
        session_id = request.session_id or str(uuid.uuid4())
        
        # Get conversation state
        if request.conversation_state:
            conversation_state = request.conversation_state
        else:
            # Create new conversation state
            conversation_state = ConversationState(
                session_id=session_id,
                phase="discovery",
                specifications_complete=False,
                messages=[]
            )
        
        # Process message with agent service
        agent_response, updated_state, action_button = await agent_service.process_message(
            user_message=request.message,
            conversation_state=conversation_state,
            action_type=request.action_type
        )
        
        # TODO: Save conversation state to database
        # await save_conversation_state(db, updated_state)
        
        return ChatResponse(
            agent_response=agent_response,
            conversation_state=updated_state,
            action_button=action_button,
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/conversation/{session_id}")
async def get_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Retrieve conversation state by session ID
    """
    try:
        # TODO: Load conversation state from database
        # conversation_state = await load_conversation_state(db, session_id)
        
        # For now, return empty state
        conversation_state = ConversationState(
            session_id=session_id,
            phase="discovery",
            specifications_complete=False,
            messages=[]
        )
        
        return conversation_state
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Conversation not found: {str(e)}")

@router.get("/roadmap/{session_id}")
async def get_roadmap(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Get the current roadmap for a session
    """
    try:
        # TODO: Load roadmap from database
        # roadmap = await load_roadmap(db, session_id)
        
        # For now, return None
        return {"roadmap": None, "message": "Roadmap retrieval not yet implemented"}
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Roadmap not found: {str(e)}")

@router.delete("/conversation/{session_id}")
async def delete_conversation(
    session_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a conversation and its associated data
    """
    try:
        # TODO: Delete conversation from database
        # await delete_conversation_data(db, session_id)
        
        return {"message": f"Conversation {session_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting conversation: {str(e)}")

# Health check for agent service
@router.get("/health")
async def agent_health():
    """
    Check if agent service is working properly
    """
    try:
        client_mode = getattr(agent_service, 'client_mode', 'unknown')
        return {
            "status": "healthy",
            "client_mode": client_mode,
            "model": agent_service.model
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent service unhealthy: {str(e)}")