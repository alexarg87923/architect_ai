from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserMessage(BaseModel):
    id: int
    content: str
    timestamp: datetime

class LLMResponse(BaseModel):
    id: int
    content: str
    timestamp: datetime

class ChatInteraction(BaseModel):
    user_message: UserMessage
    llm_response: LLMResponse

class ChatHistory(BaseModel):
    interactions: List[ChatInteraction] = []