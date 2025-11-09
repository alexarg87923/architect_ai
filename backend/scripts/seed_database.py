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
from app.services.task_service import TaskService
from app.models.api_schemas import UserCreate, ProjectCreate, TaskCreate
from app.models.database import Task as TaskDB
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
        if user_service.user_exists(db, user_data["email"]):
            logger.info(f"✅ {user_data['first_name']} {user_data['last_name']} user already exists")
            continue

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
    task_service = TaskService()

    sample_project_data = {
        "id": 1,
        "name": "new project",
        "description": "",
        "status": "draft",
        "createdAt": "2025-11-09T11:04:54.610Z",
        "updatedAt": "2025-11-09T11:04:54.610Z",
        "roadmapNodes": [
            {
                "id": 1,
                "name": "Project Setup & Environment",
                "priority": "P0",
                "description": "Establish the foundational development environment and project structure.",
                "stories": [
                    {
                        "id": 101,
                        "title": "Initialize project repository and dev tools",
                        "acceptance_criteria": [
                            "A new Git repository is created and initialized.",
                            "Basic `.gitignore` and `README.md` files are set up.",
                            "Essential development tools (e.g., code editor, npm/yarn) are ready."
                        ],
                        "completed": False
                    },
                    {
                        "id": 102,
                        "title": "Configure React frontend development environment",
                        "acceptance_criteria": [
                            "A React project is initialized using Create React App or Vite.",
                            "Frontend dependencies are installed.",
                            "A basic 'Hello World' React component is displayed in the browser."
                        ],
                        "completed": False
                    },
                    {
                        "id": 103,
                        "title": "Set up Node.js/Express backend with PostgreSQL connection",
                        "acceptance_criteria": [
                            "A Node.js project is initialized with Express.",
                            "PostgreSQL database is installed and running locally.",
                            "A database connection is successfully established from the Node.js backend.",
                            "Basic API endpoint returns a success message."
                        ],
                        "completed": False
                    }
                ]
            },
            {
                "id": 2,
                "name": "Core Frontend Development",
                "priority": "P1",
                "description": "Develop the fundamental user interface components and navigation for the portfolio.",
                "stories": [
                    {
                        "id": 201,
                        "title": "Design and implement responsive UI layout (header, navigation, footer)",
                        "acceptance_criteria": [
                            "Header with portfolio title/logo is present.",
                            "Navigation links (e.g., About, Projects, Skills) are functional.",
                            "Footer with copyright and basic links is implemented.",
                            "Layout adjusts correctly for mobile, tablet, and desktop screen sizes."
                        ],
                        "completed": False
                    },
                    {
                        "id": 202,
                        "title": "Develop clean, reusable React components",
                        "acceptance_criteria": [
                            "At least 3 core UI components (e.g., Button, Card, Section) are created.",
                            "Components follow clear naming conventions and styling guidelines.",
                            "Components are documented with prop types and basic usage examples."
                        ],
                        "completed": False
                    },
                    {
                        "id": 203,
                        "title": "Integrate routing for different portfolio sections",
                        "acceptance_criteria": [
                            "React Router is configured to manage client-side navigation.",
                            "Clicking navigation links loads the correct section component without page refresh.",
                            "URL paths accurately reflect the current section (e.g., /about, /projects)."
                        ],
                        "completed": False
                    }
                ]
            },
            {
                "id": 3,
                "name": "Backend & Database Infrastructure",
                "priority": "P2",
                "description": "Establish the server-side logic and database structure for managing portfolio content.",
                "stories": [
                    {
                        "id": 301,
                        "title": "Design PostgreSQL database schema for projects, skills, and personal info",
                        "acceptance_criteria": [
                            "Database schema includes tables for 'projects', 'skills', and 'about_me' information.",
                            "Tables have appropriate columns and data types (e.g., project_name TEXT, skill_level INT).",
                            "Relationships between tables are defined (if applicable, e.g., for project tags)."
                        ],
                        "completed": False
                    },
                    {
                        "id": 302,
                        "title": "Implement RESTful API endpoints using Node.js/Express for data retrieval",
                        "acceptance_criteria": [
                            "API endpoints are created for /api/about, /api/projects, and /api/skills.",
                            "Each endpoint successfully queries the PostgreSQL database.",
                            "Endpoints return data in a consistent JSON format."
                        ],
                        "completed": False
                    },
                    {
                        "id": 303,
                        "title": "Set up database migrations and seeding for initial data",
                        "acceptance_criteria": [
                            "A migration tool (e.g., Knex, TypeORM migrations) is configured.",
                            "Initial migrations create the defined database schema.",
                            "Seeder files populate the database with sample portfolio data (about, projects, skills)."
                        ],
                        "completed": False
                    }
                ]
            },
            {
                "id": 4,
                "name": "Portfolio Content & Display",
                "priority": "P3",
                "description": "Develop the specific sections to display personal information, projects, and skills.",
                "stories": [
                    {
                        "id": 401,
                        "title": "Create 'About Me' section to introduce self",
                        "acceptance_criteria": [
                            "The 'About Me' section displays personal information fetched from the backend.",
                            "Includes a professional photo and a concise biography.",
                            "Styling is consistent with the overall UI design."
                        ],
                        "completed": False
                    },
                    {
                        "id": 402,
                        "title": "Develop 'Projects' section to showcase detailed work",
                        "acceptance_criteria": [
                            "The 'Projects' section fetches and displays a list of projects from the backend.",
                            "Each project displays a title, description, technologies used, and a link to the live demo/repo.",
                            "Projects are presented in an appealing, scannable format (e.g., cards or grid)."
                        ],
                        "completed": False
                    },
                    {
                        "id": 403,
                        "title": "Implement 'Skills' section to list technical proficiencies",
                        "acceptance_criteria": [
                            "The 'Skills' section fetches and displays technical skills from the backend.",
                            "Skills are categorized (e.g., Frontend, Backend, Databases) or displayed visually (e.g., skill bars).",
                            "The section is easy to read and highlights key proficiencies."
                        ],
                        "completed": False
                    }
                ]
            },
            {
                "id": 5,
                "name": "Deployment & Launch",
                "priority": "P4",
                "description": "Prepare and deploy the portfolio application to a production environment.",
                "stories": [
                    {
                        "id": 501,
                        "title": "Prepare application for production deployment",
                        "acceptance_criteria": [
                            "Frontend build process generates optimized production assets.",
                            "Backend server is configured for production environment variables.",
                            "All environment-specific configurations are managed securely."
                        ],
                        "completed": False
                    },
                    {
                        "id": 502,
                        "title": "Deploy frontend and backend to a hosting service",
                        "acceptance_criteria": [
                            "Frontend is deployed to a static site host (e.g., Netlify, Vercel).",
                            "Backend API is deployed to a cloud platform (e.g., Heroku, AWS EC2, DigitalOcean).",
                            "Both frontend and backend are accessible via public URLs."
                        ],
                        "completed": False
                    },
                    {
                        "id": 503,
                        "title": "Configure domain and SSL certificate",
                        "acceptance_criteria": [
                            "A custom domain (if desired) is pointed to the deployed application.",
                            "SSL/TLS certificate is configured for secure HTTPS access.",
                            "The portfolio is fully accessible and loads securely via the custom domain."
                        ],
                        "completed": False
                    }
                ]
            }
        ],
        "tasks": {
            "daily-todos": [
                {
                    "id": 1,
                    "text": "Setup project roadmap",
                    "completed": False,
                    "archive": False
                }
            ],
            "your-ideas": [
                {
                    "id": 2,
                    "text": "Cool new idea",
                    "completed": False,
                    "archive": False
                }
            ]
        },
        "roadmap_data": {
            "project": {
                "name": "Developer Portfolio Web App",
                "vision": "To build a web application portfolio effectively showcasing development skills to recruiters, with the ultimate goal of securing a job.",
                "type": "Web Application",
                "target_users": "recruiters"
            },
            "epics": [
                {
                    "id": 1,
                    "name": "Project Setup & Environment",
                    "priority": "P0",
                    "description": "Establish the foundational development environment and project structure.",
                    "stories": [
                        {
                            "id": 101,
                            "title": "Initialize project repository and dev tools",
                            "acceptance_criteria": [
                                "A new Git repository is created and initialized.",
                                "Basic `.gitignore` and `README.md` files are set up.",
                                "Essential development tools (e.g., code editor, npm/yarn) are ready."
                            ],
                            "completed": False
                        },
                        {
                            "id": 102,
                            "title": "Configure React frontend development environment",
                            "acceptance_criteria": [
                                "A React project is initialized using Create React App or Vite.",
                                "Frontend dependencies are installed.",
                                "A basic 'Hello World' React component is displayed in the browser."
                            ],
                            "completed": False
                        },
                        {
                            "id": 103,
                            "title": "Set up Node.js/Express backend with PostgreSQL connection",
                            "acceptance_criteria": [
                                "A Node.js project is initialized with Express.",
                                "PostgreSQL database is installed and running locally.",
                                "A database connection is successfully established from the Node.js backend.",
                                "Basic API endpoint returns a success message."
                            ],
                            "completed": False
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Core Frontend Development",
                    "priority": "P1",
                    "description": "Develop the fundamental user interface components and navigation for the portfolio.",
                    "stories": [
                        {
                            "id": 201,
                            "title": "Design and implement responsive UI layout (header, navigation, footer)",
                            "acceptance_criteria": [
                                "Header with portfolio title/logo is present.",
                                "Navigation links (e.g., About, Projects, Skills) are functional.",
                                "Footer with copyright and basic links is implemented.",
                                "Layout adjusts correctly for mobile, tablet, and desktop screen sizes."
                            ],
                            "completed": False
                        },
                        {
                            "id": 202,
                            "title": "Develop clean, reusable React components",
                            "acceptance_criteria": [
                                "At least 3 core UI components (e.g., Button, Card, Section) are created.",
                                "Components follow clear naming conventions and styling guidelines.",
                                "Components are documented with prop types and basic usage examples."
                            ],
                            "completed": False
                        },
                        {
                            "id": 203,
                            "title": "Integrate routing for different portfolio sections",
                            "acceptance_criteria": [
                                "React Router is configured to manage client-side navigation.",
                                "Clicking navigation links loads the correct section component without page refresh.",
                                "URL paths accurately reflect the current section (e.g., /about, /projects)."
                            ],
                            "completed": False
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "Backend & Database Infrastructure",
                    "priority": "P2",
                    "description": "Establish the server-side logic and database structure for managing portfolio content.",
                    "stories": [
                        {
                            "id": 301,
                            "title": "Design PostgreSQL database schema for projects, skills, and personal info",
                            "acceptance_criteria": [
                                "Database schema includes tables for 'projects', 'skills', and 'about_me' information.",
                                "Tables have appropriate columns and data types (e.g., project_name TEXT, skill_level INT).",
                                "Relationships between tables are defined (if applicable, e.g., for project tags)."
                            ],
                            "completed": False
                        },
                        {
                            "id": 302,
                            "title": "Implement RESTful API endpoints using Node.js/Express for data retrieval",
                            "acceptance_criteria": [
                                "API endpoints are created for /api/about, /api/projects, and /api/skills.",
                                "Each endpoint successfully queries the PostgreSQL database.",
                                "Endpoints return data in a consistent JSON format."
                            ],
                            "completed": False
                        },
                        {
                            "id": 303,
                            "title": "Set up database migrations and seeding for initial data",
                            "acceptance_criteria": [
                                "A migration tool (e.g., Knex, TypeORM migrations) is configured.",
                                "Initial migrations create the defined database schema.",
                                "Seeder files populate the database with sample portfolio data (about, projects, skills)."
                            ],
                            "completed": False
                        }
                    ]
                },
                {
                    "id": 4,
                    "name": "Portfolio Content & Display",
                    "priority": "P3",
                    "description": "Develop the specific sections to display personal information, projects, and skills.",
                    "stories": [
                        {
                            "id": 401,
                            "title": "Create 'About Me' section to introduce self",
                            "acceptance_criteria": [
                                "The 'About Me' section displays personal information fetched from the backend.",
                                "Includes a professional photo and a concise biography.",
                                "Styling is consistent with the overall UI design."
                            ],
                            "completed": False
                        },
                        {
                            "id": 402,
                            "title": "Develop 'Projects' section to showcase detailed work",
                            "acceptance_criteria": [
                                "The 'Projects' section fetches and displays a list of projects from the backend.",
                                "Each project displays a title, description, technologies used, and a link to the live demo/repo.",
                                "Projects are presented in an appealing, scannable format (e.g., cards or grid)."
                            ],
                            "completed": False
                        },
                        {
                            "id": 403,
                            "title": "Implement 'Skills' section to list technical proficiencies",
                            "acceptance_criteria": [
                                "The 'Skills' section fetches and displays technical skills from the backend.",
                                "Skills are categorized (e.g., Frontend, Backend, Databases) or displayed visually (e.g., skill bars).",
                                "The section is easy to read and highlights key proficiencies."
                            ],
                            "completed": False
                        }
                    ]
                },
                {
                    "id": 5,
                    "name": "Deployment & Launch",
                    "priority": "P4",
                    "description": "Prepare and deploy the portfolio application to a production environment.",
                    "stories": [
                        {
                            "id": 501,
                            "title": "Prepare application for production deployment",
                            "acceptance_criteria": [
                                "Frontend build process generates optimized production assets.",
                                "Backend server is configured for production environment variables.",
                                "All environment-specific configurations are managed securely."
                            ],
                            "completed": False
                        },
                        {
                            "id": 502,
                            "title": "Deploy frontend and backend to a hosting service",
                            "acceptance_criteria": [
                                "Frontend is deployed to a static site host (e.g., Netlify, Vercel).",
                                "Backend API is deployed to a cloud platform (e.g., Heroku, AWS EC2, DigitalOcean).",
                                "Both frontend and backend are accessible via public URLs."
                            ],
                            "completed": False
                        },
                        {
                            "id": 503,
                            "title": "Configure domain and SSL certificate",
                            "acceptance_criteria": [
                                "A custom domain (if desired) is pointed to the deployed application.",
                                "SSL/TLS certificate is configured for secure HTTPS access.",
                                "The portfolio is fully accessible and loads securely via the custom domain."
                            ],
                            "completed": False
                        }
                    ]
                }
            ],
            "architecture": {
                "mermaid_diagram": "graph TD; A[Recruiter] --> B{Internet}; B --> C[React Frontend]; C -- API Requests --> D[Node.js/Express Backend]; D -- Data Access --> E[PostgreSQL Database];",
                "components": [
                    "React Frontend",
                    "Node.js/Express Backend API",
                    "PostgreSQL Database"
                ]
            },
            "message": "✅ Roadmap generated and saved! You can now start with Project Setup & Environment."
        }
    }
    
    # Sample projects for each user
    sample_projects = [
        {
            "user_email": "johndoe@example.com",
            "name": sample_project_data["name"],
            "description": sample_project_data["description"],
            "roadmap_data": sample_project_data["roadmap_data"],  # Only save the roadmap_data part, not the entire object
            "tasks": sample_project_data.get("tasks", {})  # Tasks will be created separately
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
        
        # Remove default tasks created by create_project
        db.query(TaskDB).filter(TaskDB.project_id == project.id).delete()
        db.commit()
        
        # Add roadmap data if provided
        if "roadmap_data" in project_data:
            project.roadmap_data = project_data["roadmap_data"]
            db.commit()
        
        # Create tasks from sample data if provided
        if "tasks" in project_data and project_data["tasks"]:
            tasks_data = project_data["tasks"]
            for task_type in ["daily-todos", "your-ideas"]:
                if task_type in tasks_data:
                    for task_item in tasks_data[task_type]:
                        task_create = TaskCreate(
                            text=task_item["text"],
                            completed=task_item.get("completed", False),
                            task_type=task_type
                        )
                        task_service.create_task(db, task_create, project.id)
            logger.info(f"✅ Created sample project with roadmap and tasks: {project.name} for user {project_data['user_email']} (Project ID: {project.id})")
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
