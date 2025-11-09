from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any
import json
import shutil
import os
from datetime import datetime

from app.core.database import get_db, User, Project, Conversation, Roadmap
from app.services.feedback_service import FeedbackService
from app.models.agent import UserCreate, FeedbackUpdate

router = APIRouter()
feedback_service = FeedbackService()

@router.get("/users")
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users with their project counts"""
    try:
        # Get users with project counts
        query = text("""
            SELECT 
                u.id,
                u.email,
                u.first_name,
                u.last_name,
                u.is_active,
                u.created_at,
                u.updated_at,
                COUNT(p.id) as project_count
            FROM users u
            LEFT JOIN projects p ON u.id = p.user_id
            GROUP BY u.id, u.email, u.first_name, u.last_name, u.is_active, u.created_at, u.updated_at
            ORDER BY u.created_at DESC
        """)
        
        result = db.execute(query)
        users = []
        
        for row in result:
            users.append({
                "id": row.id,
                "email": row.email,
                "first_name": row.first_name,
                "last_name": row.last_name,
                "is_active": row.is_active,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
                "project_count": row.project_count
            })
        
        return users
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {str(e)}"
        )

@router.post("/users")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        
        # Create new user
        db_user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password_hash=user_data.password,  # In production, hash this!
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return {
            "id": db_user.id,
            "email": db_user.email,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user and all their data"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete user's data in order (due to foreign key constraints)
        # Delete roadmaps
        db.query(Roadmap).filter(Roadmap.user_id == user_id).delete()
        
        # Delete messages and conversations
        db.execute(text("""
            DELETE FROM messages 
            WHERE conversation_id IN (
                SELECT id FROM conversations WHERE user_id = :user_id
            )
        """), {"user_id": user_id})
        
        db.query(Conversation).filter(Conversation.user_id == user_id).delete()
        
        # Delete projects
        db.query(Project).filter(Project.user_id == user_id).delete()
        
        # Delete user
        db.delete(user)
        
        db.commit()
        
        return {"message": "User deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )

@router.patch("/users/{user_id}/toggle-status")
async def toggle_user_status(user_id: int, status_data: dict, db: Session = Depends(get_db)):
    """Toggle user active status"""
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        user.is_active = status_data.get("is_active", not user.is_active)
        user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(user)
        
        return {
            "id": user.id,
            "is_active": user.is_active,
            "updated_at": user.updated_at
        }
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user status: {str(e)}"
        )

@router.get("/users/{user_id}/projects")
async def get_user_projects(user_id: int, db: Session = Depends(get_db)):
    """Get all projects for a specific user"""
    try:
        projects = db.query(Project).filter(Project.user_id == user_id).order_by(Project.created_at.desc()).all()
        
        return [{
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "has_roadmap": project.roadmap_data is not None
        } for project in projects]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user projects: {str(e)}"
        )

@router.get("/projects")
async def get_all_projects(db: Session = Depends(get_db)):
    """Get all projects with user information"""
    try:
        query = text("""
            SELECT 
                p.id,
                p.name,
                p.description,
                p.status,
                p.created_at,
                p.updated_at,
                p.roadmap_data,
                u.first_name || ' ' || u.last_name as user_name,
                u.email as user_email
            FROM projects p
            JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        """)
        
        result = db.execute(query)
        projects = []
        
        for row in result:
            projects.append({
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "status": row.status,
                "created_at": row.created_at,
                "updated_at": row.updated_at,
                "has_roadmap": row.roadmap_data is not None,
                "user_name": row.user_name,
                "user_email": row.user_email
            })
        
        return projects
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch projects: {str(e)}"
        )

@router.get("/analytics")
async def get_analytics(db: Session = Depends(get_db)):
    """Get system analytics"""
    try:
        # Get basic counts
        total_users = db.query(User).count()
        active_projects = db.query(Project).filter(Project.status == "active").count()
        total_roadmaps = db.query(Roadmap).count()
        total_conversations = db.query(Conversation).count()
        
        # Get projects with roadmaps
        projects_with_roadmaps = db.query(Project).filter(Project.roadmap_data.isnot(None)).count()
        
        return {
            "total_users": total_users,
            "active_projects": active_projects,
            "total_projects": db.query(Project).count(),
            "total_roadmaps": total_roadmaps,
            "total_conversations": total_conversations,
            "projects_with_roadmaps": projects_with_roadmaps,
            "roadmap_completion_rate": (projects_with_roadmaps / max(active_projects, 1)) * 100 if active_projects > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch analytics: {str(e)}"
        )

@router.post("/backup")
async def create_backup(db: Session = Depends(get_db)):
    """Create a database backup"""
    try:
        # Get the database file path
        db_path = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/roadmap.db"
        backup_dir = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/backups"
        
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"roadmap_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # Copy the database file
        shutil.copy2(db_path, backup_path)
        
        return {
            "message": "Backup created successfully",
            "backup_file": backup_filename,
            "backup_path": backup_path,
            "created_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create backup: {str(e)}"
        )

@router.get("/health")
async def system_health(db: Session = Depends(get_db)):
    """Get system health status"""
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        
        # Get database file size
        db_path = "/Users/henriquepitta/Desktop/Roadmap/agentic-backend/roadmap.db"
        db_size = os.path.getsize(db_path) if os.path.exists(db_path) else 0
        
        return {
            "status": "healthy",
            "database": "connected",
            "database_size_mb": round(db_size / 1024 / 1024, 2),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/feedback")
async def get_all_feedback(db: Session = Depends(get_db)):
    """Get all feedback (admin use)"""
    try:
        feedback_list = feedback_service.get_all_feedback(db)
        return feedback_list
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch feedback: {str(e)}"
        )

@router.patch("/feedback/{feedback_id}")
async def update_feedback(
    feedback_id: int,
    feedback_update: FeedbackUpdate,
    db: Session = Depends(get_db)
):
    """Update feedback status and admin notes (admin use)"""
    try:
        feedback = feedback_service.update_feedback(db, feedback_id, feedback_update)
        if not feedback:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        return feedback
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update feedback: {str(e)}"
        )

@router.delete("/feedback/{feedback_id}")
async def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    """Delete feedback (admin use)"""
    try:
        success = feedback_service.delete_feedback(db, feedback_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Feedback not found"
            )
        
        return {"message": "Feedback deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete feedback: {str(e)}"
        )
