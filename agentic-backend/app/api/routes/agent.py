from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.api_schemas import ConversationState, ChatMessage, Roadmap
from app.services.agent_service import AgentService
from app.services.database_service import DatabaseService
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

# Initialize AgentService and DatabaseService
agent_service = AgentService()
database_service = DatabaseService()

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
            # Try to load from database first
            conversation_state = database_service.load_conversation_state(db, session_id)
            
            if not conversation_state:
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
        
        # Save conversation state to database
        database_service.save_conversation_state(db, updated_state)
        
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
        # Load conversation state from database
        conversation_state = database_service.load_conversation_state(db, session_id)
        
        if not conversation_state:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
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
        # Load roadmap from database
        roadmap = database_service.load_roadmap(db, session_id)
        
        if roadmap:
            return {"roadmap": roadmap.dict(), "message": "Roadmap retrieved successfully"}
        else:
            return {"roadmap": None, "message": "No roadmap found for this session"}
        
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
        # Delete conversation from database
        success = database_service.delete_conversation(db, session_id)
        
        if success:
            return {"message": f"Conversation {session_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
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