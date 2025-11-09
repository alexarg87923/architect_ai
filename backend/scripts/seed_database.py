#!/usr/bin/env python3
"""
Database seeding script for Roadmap AI development

This script creates dummy users (John Doe and Becky Smith) for development testing.
Run this script to reset the database with test data.

Usage:
    # Create and populate dummy users (resets if a database exists)
    python scripts/seed_database.py
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session
from app.core.database import engine, get_db
from app.models.database import Base
from app.services.user_service import UserService
from app.services.project_service import ProjectService
from app.models.api_schemas import UserCreate, ProjectCreate
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_database():
    """Drop all tables and recreate them"""
    logger.info("🗃️ Resetting database...")
    
    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    logger.info("✅ Dropped existing tables")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Created fresh database tables")

def create_dummy_users(db: Session):
    """Create dummy users for development"""
    logger.info("👤 Creating dummy users...")
    
    user_service = UserService()
    created_users = []
    
    # Define dummy users
    dummy_users = [
        {
            "email": "johndoe@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "dev123",
            "is_superuser": True  
        },
        {
            "email": "beckysmith@example.com",
            "first_name": "Becky",
            "last_name": "Smith",
            "password": "dev123",
            "is_superuser": False  
        }
    ]
    
    for user_data in dummy_users:
        # Check if user already exists
        if user_service.user_exists(db, user_data["email"]):
            logger.info(f"✅ {user_data['first_name']} {user_data['last_name']} user already exists")
            continue
        
        # Create user
        dummy_user = UserCreate(
            email=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            password=user_data["password"],  # Simple password for development
            is_active=True
        )
        
        user = user_service.create_user(db, dummy_user, is_superuser=user_data["is_superuser"])
        logger.info(f"✅ Created dummy user: {user.email} (ID: {user.id})")
        created_users.append(user)
    
    return created_users

def create_sample_projects(db: Session, users):
    """Create sample projects for each user"""
    logger.info("📁 Creating sample projects...")
    
    project_service = ProjectService()
    
    # Pre-generated roadmap data for CodeMentor project (to save API credits)
    codementor_roadmap = {
        "project_specification": {
            "title": "CodeMentor",
            "description": "An AI-powered platform for interactive coding assistance, providing real-time feedback and guidance for learners.",
            "goals": [
                "Build the project",
                "Deploy successfully"
            ],
            "timeline_weeks": 4,
            "tech_stack": [],
            "user_experience_level": "beginner",
            "deployment_needed": True,
            "auth_needed": False,
            "commercialization_goal": False,
            "target_audience": "General users",
            "similar_projects_built": False
        },
        "nodes": [
            {
                "id": "1",
                "title": "Project Setup & Environment",
                "description": "Establish a rapid development environment with a frontend and backend setup, essential libraries, and deploy-ready configurations.",
                "subtasks": [
                    {
                        "id": "1.1",
                        "title": "Initialize Git repository",
                        "description": "Set up Git with initial commit",
                        "completed": False,
                        "estimated_hours": 2.0
                    },
                    {
                        "id": "1.2",
                        "title": "Set up frontend with React",
                        "description": "Create a new React app quickly",
                        "completed": False,
                        "estimated_hours": 2.0
                    },
                    {
                        "id": "1.3",
                        "title": "Set up backend with FastAPI",
                        "description": "Create FastAPI app with basic route",
                        "completed": False,
                        "estimated_hours": 2.0
                    },
                    {
                        "id": "1.4",
                        "title": "Create .env template file",
                        "description": "Add essential environment variables",
                        "completed": False,
                        "estimated_hours": 1.0
                    }
                ],
                "estimated_days": 1,
                "estimated_hours": 7.0,
                "tags": ["setup"],
                "dependencies": [],
                "status": "pending",
                "completion_percentage": 0,
                "deliverables": [
                    "Project structure",
                    "Development environment ready"
                ],
                "success_criteria": [
                    "All core libraries integrated",
                    "Basic project structure established"
                ],
                "overview": [
                    "Establish a local development environment using tools like Node.js and React to enable rapid prototyping and iteration.",
                    "Set up a version control system using Git, allowing for collaborative development and tracking of changes throughout the project.",
                    "Create a structured project directory that separates frontend and backend code, ensuring maintainability and scalability as the project grows.",
                    "Integrate essential libraries such as Axios for HTTP requests, React Router for navigation, and Redux for state management to streamline development.",
                    "Configure a backend server using Express.js, connecting to a database like MongoDB, to allow for user data storage and management, which lays the foundation for future features.",
                    "Implement a basic API structure to handle requests and responses, providing a clear pathway for frontend-backend communication.",
                    "Set up environment variables and configurations for seamless deployment processes, making it easier to switch between development and production environments.",
                    "Create initial frontend pages and components, such as a landing page and user dashboard, to visualize the user journey from the very beginning.",
                    "Establish a continuous integration/continuous deployment (CI/CD) pipeline to automate testing and deployment, ensuring that code changes are quickly and reliably pushed to production."
                ]
            },
            {
                "id": "2",
                "title": "User Authentication Setup",
                "description": "Implement Firebase for user authentication to allow users to create accounts and log in securely.",
                "subtasks": [
                    {
                        "id": "1",
                        "title": "Initialize React with Firebase",
                        "description": "Set up a React app with Firebase config",
                        "completed": False,
                        "estimated_hours": 2.0
                    },
                    {
                        "id": "2",
                        "title": "Implement Sign Up functionality",
                        "description": "Add user registration using Firebase Auth",
                        "completed": False,
                        "estimated_hours": 3.0
                    },
                    {
                        "id": "3",
                        "title": "Create Login page",
                        "description": "Develop a login page to authenticate users",
                        "completed": False,
                        "estimated_hours": 3.0
                    },
                    {
                        "id": "4",
                        "title": "Set up Git repository",
                        "description": "Initialize Git and add basic .env template",
                        "completed": False,
                        "estimated_hours": 2.0
                    }
                ],
                "estimated_days": 3,
                "estimated_hours": 10.0,
                "tags": ["auth"],
                "dependencies": [],
                "status": "pending",
                "completion_percentage": 0,
                "deliverables": [
                    "User registration and login functionality"
                ],
                "success_criteria": [
                    "Users can register and log in",
                    "User sessions are managed securely"
                ],
                "overview": None
            },
            {
                "id": "3",
                "title": "Integrate Interactive Code Editor",
                "description": "Set up Monaco Editor in the React frontend to provide a robust coding interface with syntax highlighting.",
                "subtasks": [
                    {
                        "id": "1",
                        "title": "Set up Monaco Editor in React",
                        "description": "Integrate Monaco Editor for syntax highlighting",
                        "completed": False,
                        "estimated_hours": 4.0
                    },
                    {
                        "id": "2",
                        "title": "Implement basic editor features",
                        "description": "Add code completion and error checking",
                        "completed": False,
                        "estimated_hours": 5.0
                    },
                    {
                        "id": "3",
                        "title": "Deploy editor to staging environment",
                        "description": "Test editor functionality in the staging area",
                        "completed": False,
                        "estimated_hours": 3.0
                    },
                    {
                        "id": "4",
                        "title": "Gather user feedback on editor",
                        "description": "Collect feedback for future enhancements",
                        "completed": False,
                        "estimated_hours": 3.0
                    }
                ],
                "estimated_days": 5,
                "estimated_hours": 15.0,
                "tags": ["frontend"],
                "dependencies": [],
                "status": "pending",
                "completion_percentage": 0,
                "deliverables": [
                    "Functional code editor integrated into the application"
                ],
                "success_criteria": [
                    "Code editor supports syntax highlighting",
                    "Basic editing features are functional"
                ],
                "overview": None
            },
            {
                "id": "4",
                "title": "Implement AI-Powered Code Analysis",
                "description": "Utilize OpenAI API to provide real-time feedback and error analysis on user code submissions.",
                "subtasks": [
                    {
                        "id": "1",
                        "title": "Set up OpenAI API integration",
                        "description": "Integrate OpenAI API for code analysis",
                        "completed": False,
                        "estimated_hours": 4.0
                    },
                    {
                        "id": "2",
                        "title": "Add real-time feedback feature",
                        "description": "Implement instant feedback on code submissions",
                        "completed": False,
                        "estimated_hours": 6.0
                    },
                    {
                        "id": "3",
                        "title": "Deploy initial prototype",
                        "description": "Deploy working model for user testing",
                        "completed": False,
                        "estimated_hours": 4.0
                    },
                    {
                        "id": "4",
                        "title": "Collect user feedback for iteration",
                        "description": "Gather insights for feature enhancements",
                        "completed": False,
                        "estimated_hours": 2.0
                    }
                ],
                "estimated_days": 7,
                "estimated_hours": 16.0,
                "tags": ["mvp"],
                "dependencies": [],
                "status": "pending",
                "completion_percentage": 0,
                "deliverables": [
                    "Code analysis and feedback feature"
                ],
                "success_criteria": [
                    "Users receive immediate feedback on code",
                    "Error analysis is accurate and helpful"
                ],
                "overview": None
            },
            {
                "id": "5",
                "title": "Develop Learning Modules",
                "description": "Create simple learning modules for Python to showcase code explanations and exercises for users.",
                "subtasks": [
                    {
                        "id": "1",
                        "title": "Set up module structure using template",
                        "description": "Create a flexible learning module structure",
                        "completed": False,
                        "estimated_hours": 4.0
                    },
                    {
                        "id": "2",
                        "title": "Implement core exercises with Python",
                        "description": "Add basic coding exercises for users",
                        "completed": False,
                        "estimated_hours": 6.0
                    },
                    {
                        "id": "3",
                        "title": "Deploy modules on learning platform",
                        "description": "Upload and configure modules for testing",
                        "completed": False,
                        "estimated_hours": 4.0
                    },
                    {
                        "id": "4",
                        "title": "Gather feedback and iterate quickly",
                        "description": "Collect user feedback to enhance modules",
                        "completed": False,
                        "estimated_hours": 6.0
                    }
                ],
                "estimated_days": 7,
                "estimated_hours": 20.0,
                "tags": ["mvp"],
                "dependencies": [],
                "status": "pending",
                "completion_percentage": 0,
                "deliverables": [
                    "Basic learning module for Python"
                ],
                "success_criteria": [
                    "Users can access learning modules",
                    "Modules provide interactive exercises and explanations"
                ],
                "overview": None
            }
        ],
        "total_estimated_weeks": 4,
        "total_estimated_hours": 68.0
    }
    
    # Sample projects for each user
    sample_projects = [
        {
            "user_email": "johndoe@example.com",
            "name": "Sample Project 1",
            "description": "A sample project for John Doe to test the roadmap functionality",
            "roadmap_data": codementor_roadmap  # Include the pre-generated roadmap
        },
        {
            "user_email": "johndoe@example.com",
            "name": "Sample Project 2",
            "description": "A second sample project for John Doe to test the roadmap functionality",
        },
        {
            "user_email": "beckysmith@example.com", 
            "name": "Sample Project 3",
            "description": "A sample project for Becky Smith to test the roadmap functionality"
        }
    ]
    
    # Create a mapping of email to user ID
    user_map = {user.email: user.id for user in users}
    
    for project_data in sample_projects:
        user_id = user_map.get(project_data["user_email"])
        if not user_id:
            logger.warning(f"⚠️ User {project_data['user_email']} not found, skipping project creation")
            continue
            
        # Create project
        sample_project = ProjectCreate(
            name=project_data["name"],
            description=project_data["description"],
            status="draft"
        )
        
        project = project_service.create_project(db, sample_project, user_id)
        
        # Add roadmap data if provided
        if "roadmap_data" in project_data:
            project.roadmap_data = project_data["roadmap_data"]
            db.commit()
            logger.info(f"✅ Created sample project with roadmap: {project.name} for user {project_data['user_email']} (Project ID: {project.id})")
        else:
            logger.info(f"✅ Created sample project: {project.name} for user {project_data['user_email']} (Project ID: {project.id})")

def main():
    """Main seeding function"""
    logger.info("🌱 Starting database seeding for Roadmap AI")
    logger.info("=" * 50)
    
    try:
        # Reset database
        reset_database()
        
        # Create database session
        db = next(get_db())
        
        try:
            # Create dummy users
            users = create_dummy_users(db)
            
            # Create sample projects for each user
            create_sample_projects(db, users)
            
            logger.info("=" * 50)
            logger.info("🎉 Database seeding completed successfully!")
            logger.info("")
            logger.info("📋 Development Users Created:")
            logger.info(f"   Email: johndoe@example.com")
            logger.info(f"   Password: dev123")
            logger.info(f"   Name: John Doe")
            logger.info(f"   Sample Project: Sample Project 1 (CodeMentor roadmap included)")
            logger.info("")
            logger.info(f"   Email: beckysmith@example.com")
            logger.info(f"   Password: dev123")
            logger.info(f"   Name: Becky Smith")
            logger.info(f"   Sample Project: Sample Project 2")
            logger.info("")
            logger.info("🚀 You can now:")
            logger.info("   1. Start the backend: uvicorn app.main:app --reload")
            logger.info("   2. Login as John Doe or Becky Smith on the frontend")
            logger.info("   3. Test all roadmap features with user context")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"❌ Error during seeding: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
