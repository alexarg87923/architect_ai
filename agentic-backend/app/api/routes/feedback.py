from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user_service import UserService
from app.services.feedback_service import FeedbackService
from app.models.agent import FeedbackCreate, FeedbackResponse
from typing import List

router = APIRouter()
user_service = UserService()
feedback_service = FeedbackService()

@router.post("/submit", response_model=FeedbackResponse)
async def submit_feedback(
    user_id: int,
    feedback_data: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    Submit feedback from user
    """
    try:
        # Verify user exists
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create feedback
        feedback = feedback_service.create_feedback(db, user_id, feedback_data)
        
        return feedback
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit feedback: {str(e)}"
        )

@router.get("/user", response_model=List[FeedbackResponse])
async def get_user_feedback(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get feedback for a specific user
    """
    try:
        # Verify user exists
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get user feedback
        feedback_list = feedback_service.get_user_feedback(db, user_id)
        
        return feedback_list
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get feedback: {str(e)}"
        ) 