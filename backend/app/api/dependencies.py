from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db

def get_database_session(db: Session = Depends(get_db)):
    return db

def get_current_user_id(user_id: int = None) -> int:
    """Helper to get current user ID - in production this would use JWT token"""
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")
    return user_id