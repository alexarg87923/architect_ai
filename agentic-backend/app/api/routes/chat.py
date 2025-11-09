from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()

class HealthCheck(BaseModel):
    status: str
    message: str

@router.get("/health", response_model=HealthCheck)
async def chat_health():
    """
    Health check for chat service
    Note: Main chat functionality is in /api/agent/chat
    """
    return HealthCheck(
        status="healthy", 
        message="Chat service is operational. Use /api/agent/chat for agent interactions."
    )

@router.get("/")
async def chat_info():
    """
    Information about chat endpoints
    """
    return {
        "message": "Chat API endpoints",
        "main_endpoint": "/api/agent/chat",
        "description": "Use the agent chat endpoint for full conversation functionality"
    }