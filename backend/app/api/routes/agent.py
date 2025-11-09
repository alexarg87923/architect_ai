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

@router.post("/conversate", response_model=ChatResponse)
async def conversate_with_agent(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Conversation endpoint for general help and task completion (does not create roadmaps)
    """
    try:
        session_id = request.conversation_state.session_id if request.conversation_state and request.conversation_state.session_id else str(uuid.uuid4())
        user_id = str(request.conversation_state.user_id) if request.conversation_state and request.conversation_state.user_id else "1"

        logger.info(f"Processing conversation request for session: {session_id} (User: {user_id})")

        existing_session = await SESSION_SERVICE.get_session(
            user_id=user_id,
            session_id=session_id,
            app_name="conversation"
        )

        if existing_session is None:
            await SESSION_SERVICE.create_session(
                app_name="conversation",
                user_id=user_id,
                state={},
                session_id=session_id
            )
            logger.info(f"Created new conversation session: {session_id}")
        else:
            logger.info(f"Using existing conversation session: {session_id}")

        story_context = ""
        if request.selected_story_ids and request.conversation_state and request.conversation_state.project_id:
            from app.models.database import Project
            project = db.query(Project).filter(Project.id == request.conversation_state.project_id).first()
            
            if project and project.roadmap_data:
                roadmap_data = project.roadmap_data
                epics = roadmap_data.get("epics", []) or roadmap_data.get("roadmapNodes", [])
                
                selected_stories = []
                for epic in epics:
                    stories = epic.get("stories", []) or epic.get("subtasks", [])
                    for story in stories:
                        if story.get("id") in request.selected_story_ids:
                            selected_stories.append({
                                "title": story.get("title", ""),
                                "acceptance_criteria": story.get("acceptance_criteria", [])
                            })
                
                if selected_stories:
                    story_context = "\n\nSelected Stories Context:\n"
                    for idx, story in enumerate(selected_stories, 1):
                        story_context += f"\n{idx}. {story['title']}\n"
                        if story.get("acceptance_criteria"):
                            story_context += "   Acceptance Criteria:\n"
                            for ac in story["acceptance_criteria"]:
                                story_context += f"   - {ac}\n"

        user_message = request.message
        if story_context:
            user_message = f"{story_context}\n\nUser Question: {request.message}"
        
        user_content = Content(parts=[Part(text=user_message)])

        from app.agents.agent import conversation_agent

        runner = Runner(
            app_name="conversation",
            agent=conversation_agent,
            session_service=SESSION_SERVICE
        )

        agent_response_parts = []

        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_content):
            logger.debug(f"Conversation agent event: author={event.author}")

            if event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        agent_response_parts.append(part.text)

        agent_response = "\n".join(agent_response_parts) if agent_response_parts else "I'm here to help! How can I assist you?"

        session = await SESSION_SERVICE.get_session(
            user_id=user_id,
            session_id=session_id,
            app_name="conversation"
        )

        adk_state = dict(session.state) if session and session.state else {}

        if request.conversation_state:
            messages = request.conversation_state.messages.copy()
        else:
            messages = []

        messages.append(ChatMessage(role="user", content=request.message))
        messages.append(ChatMessage(role="assistant", content=agent_response))

        project_id = request.conversation_state.project_id if request.conversation_state and request.conversation_state.project_id else None

        updated_state = ConversationState(
            session_id=session_id,
            user_id=int(user_id),
            project_id=project_id,
            phase=request.conversation_state.phase if request.conversation_state else "editing",
            specifications_complete=request.conversation_state.specifications_complete if request.conversation_state else True,
            project_specification=request.conversation_state.project_specification if request.conversation_state else None,
            current_roadmap=request.conversation_state.current_roadmap if request.conversation_state else None,
            messages=messages,
            nodes_needing_subtasks=[]
        )

        save_success = database_service.save_conversation_state(db, updated_state)

        if save_success:
            logger.info(f"Conversation saved for session {session_id}")
        else:
            logger.error(f"Failed to save conversation state for session {session_id}")

        return ChatResponse(
            agent_response=agent_response,
            conversation_state=updated_state,
            action_button=None,
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"Error processing conversation: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing conversation: {str(e)}")

@router.post("/roadmap", response_model=ChatResponse)
async def create_roadmap(
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
        raw_response = "\n".join(agent_response_parts) if agent_response_parts else "Processing your request..."

        # Parse JSON response(s) and extract message field(s) if it's structured output
        import json
        agent_response = raw_response
        extracted_messages = []

        # Try to parse each response part individually (in case multiple agents respond)
        for part in agent_response_parts:
            try:
                parsed_response = json.loads(part)
                if isinstance(parsed_response, dict) and "message" in parsed_response:
                    extracted_messages.append(parsed_response["message"])
                    logger.debug(f"Extracted message from JSON response part")
                else:
                    # JSON but no message field, use raw part
                    extracted_messages.append(part)
            except (json.JSONDecodeError, ValueError):
                # Not JSON, use raw part
                extracted_messages.append(part)

        # If we successfully extracted any messages, use them; otherwise use raw response
        if extracted_messages:
            agent_response = "\n\n".join(extracted_messages)
        else:
            agent_response = raw_response

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

        # Get project_id from incoming conversation state if available
        project_id = request.conversation_state.project_id if request.conversation_state and request.conversation_state.project_id else None

        # Create updated conversation state
        updated_state = ConversationState(
            session_id=session_id,
            user_id=int(user_id),  # Use the user_id variable already set at the top
            project_id=project_id,  # Link conversation to project
            phase=phase,
            specifications_complete=context_complete,
            project_specification=current_roadmap.project if current_roadmap else None,
            current_roadmap=current_roadmap,
            messages=messages,
            nodes_needing_subtasks=[]
        )

        # Save conversation state to database (this also saves the roadmap internally)
        save_success = database_service.save_conversation_state(db, updated_state)

        if save_success:
            logger.info(f"Conversation and roadmap saved for session {session_id}")
        else:
            logger.error(f"Failed to save conversation state for session {session_id}")

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
