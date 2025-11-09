from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.models.api_schemas import ConversationState, ChatMessage, Roadmap, ChatRequest, ChatResponse
from app.services import database_service
import uuid
from datetime import datetime
import logging
import os

# Set Google API key in environment before importing agent
from app.core.config import settings
os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY

# Google ADK imports
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai.types import Content, Part
from app.agents.agent import project_roadmap_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()

# Global session service to maintain ADK sessions
# Using DatabaseSessionService for persistence across restarts and multiple workers
SESSION_SERVICE = DatabaseSessionService(db_url=settings.DATABASE_URL)

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint that handles all agent interactions using Google ADK agent
    """
    try:
        # Get or create session identifiers
        session_id = request.conversation_state.session_id if request.conversation_state and request.conversation_state.session_id else str(uuid.uuid4())
        user_id = str(request.conversation_state.user_id) if request.conversation_state and request.conversation_state.user_id else "1"

        logger.info(f"Processing chat request for session: {session_id} (User: {user_id})")

        # Check if session exists (get_session returns None if not found, doesn't raise exception)
        existing_session = await SESSION_SERVICE.get_session(
            user_id=user_id,
            session_id=session_id,
            app_name="agents"
        )

        if existing_session is None:
            # Create session if it doesn't exist (first message in conversation)
            await SESSION_SERVICE.create_session(
                app_name="agents",
                user_id=user_id,
                state={},
                session_id=session_id
            )
            logger.info(f"Created new ADK session: {session_id}")
        else:
            logger.info(f"Using existing ADK session: {session_id}")

        # Create user message content
        user_content = Content(parts=[Part(text=request.message)])

        # Run the agent (Runner setup uses the correct app_name)
        runner = Runner(
            app_name="agents",
            agent=project_roadmap_orchestrator,
            session_service=SESSION_SERVICE
        )

        # Collect agent responses
        agent_response_parts = []

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_content):
            logger.debug(f"Agent event: author={event.author}")

            # Collect responses from any sub-agent
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        agent_response_parts.append(part.text)

        # Combine all response parts
        agent_response = "\n".join(agent_response_parts) if agent_response_parts else "Processing your request..."

        # Get updated session to extract state
        session = await SESSION_SERVICE.get_session(
            user_id=user_id,
            session_id=session_id,
            app_name="agents"
        )

        # Extract session state
        adk_state = dict(session.state) if session and session.state else {}

        logger.info(f"ADK session state keys: {list(adk_state.keys())}")

        # Determine phase from conversation stage
        adk_stage = adk_state.get("conversation_stage", "vision_clarification")
        final_status = adk_state.get("final_status", {})
        context_complete = final_status.get("context_gathering_complete", False) if isinstance(final_status, dict) else False

        # Map ADK stage to backend phase
        stage_map = {
            "vision_clarification": "discovery",
            "project_type_classification": "discovery",
            "requirements_gathering": "discovery",
            "epic_planning": "confirmation",
            "architecture_design": "confirmation",
            "final_validation": "generation",
        }
        phase = stage_map.get(adk_stage, "discovery")

        # Check if roadmap has been generated
        final_roadmap = adk_state.get("final_roadmap")
        roadmap_generated = final_roadmap is not None

        if roadmap_generated:
            phase = "editing"

        # Create/update conversation state
        if request.conversation_state:
            messages = request.conversation_state.messages.copy()
        else:
            messages = []

        messages.append(ChatMessage(role="user", content=request.message))
        messages.append(ChatMessage(role="assistant", content=agent_response))

        # Parse roadmap if generated
        current_roadmap = None
        if roadmap_generated and final_roadmap:
            try:
                current_roadmap = Roadmap(**final_roadmap)
                logger.info("Successfully parsed roadmap from agent")
            except Exception as e:
                logger.error(f"Error parsing roadmap: {e}", exc_info=True)

        # Create updated conversation state
        updated_state = ConversationState(
            session_id=session_id,
            user_id=request.conversation_state.user_id if request.conversation_state else None,
            phase=phase,
            specifications_complete=context_complete,
            project_specification=current_roadmap.project if current_roadmap else None,
            current_roadmap=current_roadmap,
            messages=messages,
            nodes_needing_subtasks=[]
        )

        # Save conversation state to database
        database_service.save_conversation_state(db, updated_state)

        # Save roadmap if generated
        if current_roadmap:
            database_service.save_roadmap(db, session_id, current_roadmap, updated_state.user_id)

        return ChatResponse(
            agent_response=agent_response,
            conversation_state=updated_state,
            action_button=None,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)
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

# Health check for agent
@router.get("/health")
async def agent_health():
    """
    Check if agent is working properly
    """
    try:
        return {
            "status": "healthy",
            "agent": "Google ADK",
            "model": "gemini-2.5-flash"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent unhealthy: {str(e)}")
