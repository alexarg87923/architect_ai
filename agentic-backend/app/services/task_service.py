from sqlalchemy.orm import Session
from app.core.database import Task as TaskDB
from app.models.agent import TaskCreate, TaskUpdate
from typing import List, Optional, Dict
from datetime import datetime

class TaskService:
    """Service for handling task CRUD operations"""
    
    def create_task(self, db: Session, task_data: TaskCreate, project_id: int) -> TaskDB:
        """Create a new task for a project"""
        db_task = TaskDB(
            project_id=project_id,
            text=task_data.text,
            completed=task_data.completed,
            task_type=task_data.task_type
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    
    def get_project_tasks(self, db: Session, project_id: int) -> Dict[str, List[TaskDB]]:
        """Get all tasks for a project, grouped by type"""
        tasks = db.query(TaskDB).filter(
            TaskDB.project_id == project_id
        ).order_by(TaskDB.created_at.asc()).all()
        
        # Group tasks by type
        tasks_by_type = {
            "daily-todos": [],
            "your-ideas": []
        }
        
        for task in tasks:
            if task.task_type in tasks_by_type:
                tasks_by_type[task.task_type].append(task)
        
        return tasks_by_type
    
    def get_task(self, db: Session, task_id: int, project_id: int) -> Optional[TaskDB]:
        """Get a specific task by ID for a project"""
        return db.query(TaskDB).filter(
            TaskDB.id == task_id,
            TaskDB.project_id == project_id
        ).first()
    
    def update_task(self, db: Session, task_id: int, project_id: int, task_update: TaskUpdate) -> Optional[TaskDB]:
        """Update a task"""
        db_task = self.get_task(db, task_id, project_id)
        if not db_task:
            return None
        
        # Update fields if provided
        if task_update.text is not None:
            db_task.text = task_update.text
        if task_update.completed is not None:
            db_task.completed = task_update.completed
        if task_update.task_type is not None:
            db_task.task_type = task_update.task_type
        
        db_task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_task)
        return db_task
    
    def delete_task(self, db: Session, task_id: int, project_id: int) -> bool:
        """Delete a task"""
        db_task = self.get_task(db, task_id, project_id)
        if not db_task:
            return False
        
        db.delete(db_task)
        db.commit()
        return True
    
    def task_exists(self, db: Session, task_id: int, project_id: int) -> bool:
        """Check if a task exists for a project"""
        return self.get_task(db, task_id, project_id) is not None 