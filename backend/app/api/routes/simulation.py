"""
Simulation endpoints for LLM-to-LLM conversation testing
"""
import os
import json
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.database_service import DatabaseService
from app.services.user_service import UserService
from app.services.user_simulation_service.conversation_orchestrator import ConversationOrchestrator
from app.services.user_simulation_service.project_prompts import get_available_project_types, PROJECT_DEFINITIONS

router = APIRouter()

# Initialize services
database_service = DatabaseService()
conversation_orchestrator = ConversationOrchestrator()
user_service = UserService()

def cleanup_user_data(user_id: int, target_project_id: int):
    """Clean up existing roadmaps and conversations for a user, and clear roadmap data from target project"""
    try:
        # Connect to the database
        db_path = os.path.join(os.path.dirname(__file__), "../../../roadmap.db")
        # Ensure the path is absolute
        db_path = os.path.abspath(db_path)
        print(f"🔍 Database path: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Delete related roadmaps and conversations for this user
        cursor.execute("DELETE FROM roadmaps WHERE user_id = ?", (user_id,))
        cursor.execute("""
            DELETE FROM messages WHERE conversation_id IN (
                SELECT id FROM conversations WHERE user_id = ?
            )
        """, (user_id,))
        cursor.execute("DELETE FROM conversations WHERE user_id = ?", (user_id,))
        
        # Clear roadmap data from the target project
        cursor.execute("""
            UPDATE projects 
            SET roadmap_data = NULL, updated_at = datetime('now')
            WHERE id = ? AND user_id = ?
        """, (target_project_id, user_id))
        
        rows_affected = cursor.rowcount
        print(f"🗑️ Cleared roadmap data from project {target_project_id} (rows affected: {rows_affected})")
        
        conn.commit()
        conn.close()
        
        print(f"✅ Cleanup complete for project {target_project_id}")
        return None
        
    except Exception as e:
        print(f"❌ Failed to cleanup user data: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise e

@router.get("/simulation/project-options")
async def get_project_options():
    """
    Get available project types for simulation
    Returns list of project types with their details
    """
    try:
        available_types = get_available_project_types()
        
        # Get detailed information for each project type
        project_options = []
        for project_type in available_types:
            if project_type in PROJECT_DEFINITIONS:
                project_info = PROJECT_DEFINITIONS[project_type]
                project_options.append({
                    "value": project_type,
                    "label": project_info["name"],
                    "description": project_info["description"],
                    "tech_experience": project_info["tech_experience"]
                })
        
        return {
            "success": True,
            "project_options": project_options
        }
        
    except Exception as e:
        print(f"❌ Failed to get project options: {e}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to get project options: {str(e)}")

@router.post("/simulation/run")
async def run_simulation(
    user_id: int,
    project_id: int,
    project_type: str = "codementor",
    db: Session = Depends(get_db)
):
    """
    Run a complete LLM-to-LLM conversation simulation
    Returns the full conversation and generated roadmap
    """
    try:
        # Verify user exists
        if not user_service.user_exists_by_id(db, user_id):
            raise HTTPException(status_code=404, detail="User not found")
        
        # Clean up existing data for this user and clear roadmap from target project
        cleanup_user_data(user_id, project_id)
        
        # Run the simulation
        result = await conversation_orchestrator.run_simulation(user_id, project_type)
        
        # Save the conversation state to database
        if result["conversation_state"]:
            database_service.save_conversation_state(db, result["conversation_state"])
        
        print(f"🔍 About to link roadmap to project...")
        # Link the roadmap to the project
        print(f"🔍 About to link roadmap to project...")
        print(f"🔍 Checking if roadmap exists in result: {result.get('roadmap') is not None}")
        print(f"🔍 Result keys: {list(result.keys())}")
        print(f"🔍 Roadmap type: {type(result.get('roadmap'))}")
        if result.get("roadmap"):
            print(f"🔍 Roadmap found, attempting to link to project")
            try:
                # Connect to database and update project with roadmap
                db_path = os.path.join(os.path.dirname(__file__), "../../../roadmap.db")
                db_path = os.path.abspath(db_path)
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Update project with roadmap data using the passed project_id
                # Convert Roadmap object to dict if needed
                roadmap_data = result["roadmap"]
                print(f"🔍 Roadmap data type: {type(roadmap_data)}")
                if hasattr(roadmap_data, 'dict'):
                    roadmap_data = roadmap_data.dict()
                    print(f"🔍 Converted using .dict()")
                elif hasattr(roadmap_data, '__dict__'):
                    roadmap_data = roadmap_data.__dict__
                    print(f"🔍 Converted to __dict__")
                else:
                    print(f"🔍 Using roadmap_data as-is")
                
                roadmap_json = json.dumps(roadmap_data)
                print(f"🔍 Roadmap JSON length: {len(roadmap_json)}")
                
                cursor.execute("""
                    UPDATE projects 
                    SET roadmap_data = ?, updated_at = datetime('now')
                    WHERE id = ? AND user_id = ?
                """, (roadmap_json, project_id, user_id))
                
                rows_affected = cursor.rowcount
                print(f"🔍 Rows affected by UPDATE: {rows_affected}")
                
                # Also create a roadmap record
                cursor.execute("""
                    INSERT INTO roadmaps (user_id, roadmap_data, created_at, updated_at)
                    VALUES (?, ?, datetime('now'), datetime('now'))
                """, (user_id, roadmap_json))
                
                conn.commit()
                conn.close()
                print(f"✅ Roadmap linked to project (ID: {project_id})")
            except Exception as e:
                print(f"❌ Failed to link roadmap to project: {e}")
                import traceback
                print(f"❌ Full traceback: {traceback.format_exc()}")
        else:
            print("❌ No roadmap found in result")
        
        return {
            "success": True,
            "session_id": result["session_id"],
            "conversation_state": result["conversation_state"],
            "messages": result["messages"],
            "roadmap": result["roadmap"],
            "total_rounds": result["total_rounds"],
            "project_id": project_id
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Simulation failed: {str(e)}")
        print(f"❌ Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}") 