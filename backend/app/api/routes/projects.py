# Standard library imports
from typing import List

# Third-party imports
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

# Local imports
from app.core.database import get_db
from app.api.dependencies import get_current_user_id
from app.models.api_schemas import ProjectCreate, ProjectUpdate, ProjectResponse, Roadmap, TaskCreate, TaskUpdate, TaskResponse, TasksByType
from app.services import project_service, task_service, user_service

router = APIRouter()

@router.post("/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new project for the authenticated user"""
    try:
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        db_project = project_service.create_project(db, project, user_id)
        
        tasks_by_type = task_service.get_project_tasks(db, db_project.id)
        
        tasks_response = TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["your-ideas"]]
        )
        
        return ProjectResponse(
            id=db_project.id,
            name=db_project.name,
            description=db_project.description,
            status=db_project.status,
            roadmap_data=None,
            tasks=tasks_response,
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
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        projects = project_service.get_user_projects(db, user_id)
        
        response_projects = []
        for project in projects:
            tasks_by_type = task_service.get_project_tasks(db, project.id)
            
            tasks_response = TasksByType(
                daily_todos=[TaskResponse(
                    id=task.id,
                    project_id=task.project_id,
                    text=task.text,
                    completed=task.completed,
                    task_type=task.task_type,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    archive=task.archive or False,
                ) for task in tasks_by_type["daily-todos"]],
                your_ideas=[TaskResponse(
                    id=task.id,
                    project_id=task.project_id,
                    text=task.text,
                    completed=task.completed,
                    task_type=task.task_type,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    archive=task.archive or False,
                ) for task in tasks_by_type["your-ideas"]]
            )
            
            response_projects.append(ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                status=project.status,
                roadmap_data=Roadmap(**project.roadmap_data) if project.roadmap_data else None,
                tasks=tasks_response,
                created_at=project.created_at,
                updated_at=project.updated_at
            ))
        
        return response_projects
        
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
        
        tasks_by_type = task_service.get_project_tasks(db, project.id)
        
        tasks_response = TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["your-ideas"]]
        )
        
        return ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            roadmap_data=Roadmap(**project.roadmap_data) if project.roadmap_data else None,
            tasks=tasks_response,
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
        
        tasks_by_type = task_service.get_project_tasks(db, updated_project.id)
        
        tasks_response = TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["your-ideas"]]
        )
        
        return ProjectResponse(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            status=updated_project.status,
            roadmap_data=Roadmap(**updated_project.roadmap_data) if updated_project.roadmap_data else None,
            tasks=tasks_response,
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
        
        tasks_by_type = task_service.get_project_tasks(db, updated_project.id)
        
        tasks_response = TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["your-ideas"]]
        )
        
        return ProjectResponse(
            id=updated_project.id,
            name=updated_project.name,
            description=updated_project.description,
            status=updated_project.status,
            roadmap_data=Roadmap(**updated_project.roadmap_data) if updated_project.roadmap_data else None,
            tasks=tasks_response,
            created_at=updated_project.created_at,
            updated_at=updated_project.updated_at
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project roadmap: {str(e)}")

@router.post("/projects/{project_id}/tasks", response_model=TaskResponse)
async def create_task(
    project_id: int,
    task: TaskCreate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Create a new task for a project"""
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        if task.task_type not in ["daily-todos", "your-ideas"]:
            raise HTTPException(status_code=400, detail="Task type must be 'daily-todos' or 'your-ideas'")
        
        db_task = task_service.create_task(db, task, project_id)
        
        return TaskResponse(
            id=db_task.id,
            project_id=db_task.project_id,
            text=db_task.text,
            completed=db_task.completed,
            task_type=db_task.task_type,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            archive=False,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

@router.put("/projects/{project_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    project_id: int,
    task_id: int,
    task_update: TaskUpdate,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Update a task"""
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        updated_task = task_service.update_task(db, task_id, project_id, task_update)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return TaskResponse(
            id=updated_task.id,
            project_id=updated_task.project_id,
            text=updated_task.text,
            completed=updated_task.completed,
            task_type=updated_task.task_type,
            created_at=updated_task.created_at,
            updated_at=updated_task.updated_at,
            archive=updated_task.archive or False,
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

@router.delete("/projects/{project_id}/tasks/{task_id}")
async def delete_task(
    project_id: int,
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Delete a task"""
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        success = task_service.delete_task(db, task_id, project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        
        return {"message": f"Task {task_id} deleted successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")

@router.get("/projects/{project_id}/tasks", response_model=TasksByType)
async def get_project_tasks(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get all tasks for a project"""
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        tasks_by_type = task_service.get_project_tasks(db, project_id)
        
        return TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in tasks_by_type["your-ideas"]]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching tasks: {str(e)}")

@router.patch("/projects/{project_id}/tasks/{task_id}/archive")    
async def archive_task(
    project_id: int,
    task_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Archive a task"""
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        success = task_service.archive_task(db, task_id, project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": f"Task {task_id} archived successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error archiving task: {str(e)}")
    
@router.get("/projects/{project_id}/tasks/archived")
async def get_archived_tasks(
    project_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Get archived tasks for a project""" 
    try:
        if not project_service.project_exists(db, project_id, user_id):
            raise HTTPException(status_code=404, detail="Project not found")
        
        all_tasks = task_service.get_project_tasks(db, project_id, include_archived=True)

        archived_tasks = {
            "daily-todos": [task for task in all_tasks["daily-todos"] if task.archive],
            "your-ideas": [task for task in all_tasks["your-ideas"] if task.archive]
        }

        return TasksByType(
            daily_todos=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in archived_tasks["daily-todos"]],
            your_ideas=[TaskResponse(
                id=task.id,
                project_id=task.project_id,
                text=task.text,
                completed=task.completed,
                task_type=task.task_type,
                created_at=task.created_at,
                updated_at=task.updated_at,
                archive=task.archive or False,
            ) for task in archived_tasks["your-ideas"]]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching archived tasks: {str(e)}")