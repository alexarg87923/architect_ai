from sqlalchemy.orm import Session
from app.core.database import Project as ProjectDB, Task as TaskDB
from app.models.agent import ProjectCreate, ProjectUpdate, Roadmap, TasksByType, TaskResponse
from typing import List, Optional
from datetime import datetime
import json

class ProjectService:
    """Service for handling project CRUD operations"""
    
    def create_project(self, db: Session, project_data: ProjectCreate, user_id: int) -> ProjectDB:
        """Create a new project for a user with default tasks"""
        db_project = ProjectDB(
            user_id=user_id,
            name=project_data.name,
            description=project_data.description,
            status=project_data.status
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        
        # Create default tasks for the new project
        default_tasks = [
            {
                "text": "Setup project roadmap",
                "task_type": "daily-todos",
                "completed": False
            },
            {
                "text": "Cool new idea",
                "task_type": "your-ideas", 
                "completed": False
            }
        ]
        
        for task_data in default_tasks:
            db_task = TaskDB(
                project_id=db_project.id,
                text=task_data["text"],
                completed=task_data["completed"],
                task_type=task_data["task_type"]
            )
            db.add(db_task)
        
        db.commit()
        return db_project
    
    def get_user_projects(self, db: Session, user_id: int) -> List[ProjectDB]:
        """Get all projects for a user"""
        return db.query(ProjectDB).filter(
            ProjectDB.user_id == user_id
        ).order_by(ProjectDB.created_at.asc()).all()
    
    def get_project(self, db: Session, project_id: int, user_id: int) -> Optional[ProjectDB]:
        """Get a specific project by ID for a user"""
        return db.query(ProjectDB).filter(
            ProjectDB.id == project_id,
            ProjectDB.user_id == user_id
        ).first()
    
    def update_project(self, db: Session, project_id: int, user_id: int, project_update: ProjectUpdate) -> Optional[ProjectDB]:
        """Update a project"""
        db_project = self.get_project(db, project_id, user_id)
        if not db_project:
            return None
        
        # Update fields if provided
        if project_update.name is not None:
            db_project.name = project_update.name
        if project_update.description is not None:
            db_project.description = project_update.description
        if project_update.status is not None:
            db_project.status = project_update.status
        if project_update.roadmap_data is not None:
            # Convert Pydantic model to dict for JSON storage
            db_project.roadmap_data = project_update.roadmap_data.dict()
        
        db_project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def delete_project(self, db: Session, project_id: int, user_id: int) -> bool:
        """Delete a project"""
        db_project = self.get_project(db, project_id, user_id)
        if not db_project:
            return False
        
        db.delete(db_project)
        db.commit()
        return True
    
    def update_project_roadmap(self, db: Session, project_id: int, user_id: int, roadmap: Roadmap) -> Optional[ProjectDB]:
        """Update the roadmap for a project"""
        db_project = self.get_project(db, project_id, user_id)
        if not db_project:
            return None
        
        db_project.roadmap_data = roadmap.dict()
        db_project.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_project)
        return db_project
    
    def project_exists(self, db: Session, project_id: int, user_id: int) -> bool:
        """Check if a project exists for a user"""
        return self.get_project(db, project_id, user_id) is not None
    
    def get_project_with_tasks(self, db: Session, project_id: int, user_id: int) -> Optional[ProjectDB]:
        """Get a project with its tasks included"""
        db_project = self.get_project(db, project_id, user_id)
        if not db_project:
            return None
        
        # Load tasks for the project
        tasks = db_project.tasks
        
        # Group tasks by type
        tasks_by_type = {
            "daily-todos": [],
            "your-ideas": []
        }
        
        for task in tasks:
            if task.task_type in tasks_by_type:
                tasks_by_type[task.task_type].append(task)
        
        # Add tasks to project object for easy access
        db_project.tasks_by_type = tasks_by_type
        
        return db_project
