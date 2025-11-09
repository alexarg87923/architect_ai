from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class FeedbackBase(BaseModel):
    """Base feedback model with common fields"""
    feedback_type: str  # "general", "bug", "feature", "improvement"
    message: str

class FeedbackCreate(FeedbackBase):
    """Model for creating new feedback"""
    pass

class FeedbackUpdate(BaseModel):
    """Model for updating feedback (admin use)"""
    status: Optional[str] = None
    admin_notes: Optional[str] = None

class Feedback(FeedbackBase):
    """Complete feedback model with ID and timestamps"""
    id: int
    user_id: int
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class FeedbackResponse(BaseModel):
    """Feedback response model for API responses"""
    id: int
    user_id: int
    feedback_type: str
    message: str
    status: str
    admin_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    user_email: Optional[str] = None
    user_name: Optional[str] = None
