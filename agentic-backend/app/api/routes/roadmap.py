from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class HealthCheck(BaseModel):
    status: str
    message: str

@router.get("/health", response_model=HealthCheck)
async def roadmap_health():
    """
    Health check for roadmap service
    Note: Main roadmap functionality is in /api/agent/chat
    """
    return HealthCheck(
        status="healthy", 
        message="Roadmap service is operational. Use /api/agent/chat for roadmap generation."
    )

@router.get("/")
async def roadmap_info():
    """
    Information about roadmap endpoints
    """
    return {
        "message": "Roadmap API endpoints",
        "main_endpoint": "/api/agent/chat",
        "get_roadmap": "/api/agent/roadmap/{session_id}",
        "description": "Use the agent chat endpoint for roadmap generation and editing"
    }