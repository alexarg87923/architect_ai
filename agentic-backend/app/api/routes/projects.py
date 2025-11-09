from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.agent import ProjectCreate, ProjectUpdate, ProjectResponse, Roadmap
from app.services.project_service import ProjectService
from app.services.user_service import UserService

router = APIRouter()
project_service = ProjectService()
user_service = UserService()

def get_current_user_id(user_id: int = None) -> int:
    """Helper to get current user ID - in production this would use JWT token"""
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID required")
    return user_id

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new project for the authenticated user"""
    try:
        # Verify user exists
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create project
        db_project = project_service.create_project(db, project, user_id)
        
        # Convert to response format
        return ProjectResponse(
            id=db_project.id,
            name=db_project.name,
            description=db_project.description,
            status=db_project.status,
            roadmap_data=None,  # New projects start with no roadmap
            created_at=db_project.created_at,
            updated_at=db_project.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {str(e)}")

@router.get("/projects", response_model=List[ProjectResponse])
async def get_user_projects(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all projects for the authenticated user"""
    try:
        # Verify user exists
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get projects
        projects = project_service.get_user_projects(db, user_id)
        
        # Convert to response format
        return [
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                status=project.status,
                roadmap_data=Roadmap(**project.roadmap_data) if project.roadmap_data else None,
                created_at=project.created_at,
                updated_at=project.updated_at
            )
            for project in projects
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {str(e)}")

@router.get("/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project by ID"""
    try:
        project = project_service.get_project(db, project_id, user_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            roadmap_data=Roadmap(**project.roadmap_data) if project.roadmap_data else None,
            created_at=project.created_at,
            updated_at=project.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {str(e)}")

@router.put("/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update a project"""
    try:
        updated_project = project_service.update_project(db, project_id, user_id, project_update)
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            status=updated_project.status,
            roadmap_data=Roadmap(**updated_project.roadmap_data) if updated_project.roadmap_data else None,
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project: {str(e)}")

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project"""
    try:
        success = project_service.delete_project(db, project_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": f"Project {project_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")

@router.put("/projects/{project_id}/roadmap", response_model=ProjectResponse)
async def update_project_roadmap(
    project_id: int,
    roadmap: Roadmap,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update the roadmap for a project"""
    try:
        updated_project = project_service.update_project_roadmap(db, project_id, user_id, roadmap)
        if not updated_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return ProjectResponse(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            status=updated_project.status,
            roadmap_data=Roadmap(**updated_project.roadmap_data) if updated_project.roadmap_data else None,
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project roadmap: {str(e)}")
