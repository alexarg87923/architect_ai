from sqlalchemy.orm import Session
from app.core.database import Feedback as FeedbackDB, User as UserDB
from app.models.agent import FeedbackCreate, FeedbackUpdate, FeedbackResponse
from typing import List, Optional
from datetime import datetime

class FeedbackService:
    """Service for handling feedback operations"""
    
    def create_feedback(self, db: Session, user_id: int, feedback_create: FeedbackCreate) -> FeedbackResponse:
        """Create new feedback"""
        db_feedback = FeedbackDB(
            user_id=user_id,
            feedback_type=feedback_create.feedback_type,
            message=feedback_create.message,
            status="pending"
        )
        
        db.add(db_feedback)
        db.commit()
        db.refresh(db_feedback)
        
        return self._to_response(db_feedback, db)
    
    def get_all_feedback(self, db: Session) -> List[FeedbackResponse]:
        """Get all feedback (admin use)"""
        db_feedback_list = db.query(FeedbackDB).order_by(FeedbackDB.created_at.desc()).all()
        return [self._to_response(feedback, db) for feedback in db_feedback_list]
    
    def get_user_feedback(self, db: Session, user_id: int) -> List[FeedbackResponse]:
        """Get feedback for a specific user"""
        db_feedback_list = db.query(FeedbackDB).filter(FeedbackDB.user_id == user_id).order_by(FeedbackDB.created_at.desc()).all()
        return [self._to_response(feedback, db) for feedback in db_feedback_list]
    
    def get_feedback_by_id(self, db: Session, feedback_id: int) -> Optional[FeedbackResponse]:
        """Get feedback by ID"""
        db_feedback = db.query(FeedbackDB).filter(FeedbackDB.id == feedback_id).first()
        if not db_feedback:
            return None
        return self._to_response(db_feedback, db)
    
    def update_feedback(self, db: Session, feedback_id: int, feedback_update: FeedbackUpdate) -> Optional[FeedbackResponse]:
        """Update feedback (admin use)"""
        db_feedback = db.query(FeedbackDB).filter(FeedbackDB.id == feedback_id).first()
        if not db_feedback:
            return None
        
        # Update fields
        if feedback_update.status is not None:
            db_feedback.status = feedback_update.status
        if feedback_update.admin_notes is not None:
            db_feedback.admin_notes = feedback_update.admin_notes
        
        db_feedback.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_feedback)
        
        return self._to_response(db_feedback, db)
    
    def delete_feedback(self, db: Session, feedback_id: int) -> bool:
        """Delete feedback"""
        db_feedback = db.query(FeedbackDB).filter(FeedbackDB.id == feedback_id).first()
        if not db_feedback:
            return False
        
        db.delete(db_feedback)
        db.commit()
        return True
    
    def _to_response(self, db_feedback: FeedbackDB, db: Session) -> FeedbackResponse:
        """Convert database feedback to response model"""
        # Get user info
        user = db.query(UserDB).filter(UserDB.id == db_feedback.user_id).first()
        user_email = user.email if user else None
        user_name = f"{user.first_name} {user.last_name}" if user and user.first_name and user.last_name else None
        
        return FeedbackResponse(
            id=db_feedback.id,
            user_id=db_feedback.user_id,
            feedback_type=db_feedback.feedback_type,
            message=db_feedback.message,
            status=db_feedback.status,
            admin_notes=db_feedback.admin_notes,
            created_at=db_feedback.created_at,
            updated_at=db_feedback.updated_at,
            user_email=user_email,
            user_name=user_name
        ) 