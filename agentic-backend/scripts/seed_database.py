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
    
    # Sample projects for each user
    sample_projects = [
        {
            "user_email": "johndoe@example.com",
            "name": "Sample Project 1",
            "description": "A sample project for John Doe to test the roadmap functionality"
        },
        {
            "user_email": "beckysmith@example.com", 
            "name": "Sample Project 2",
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
            logger.info(f"   Sample Project: Sample Project 1")
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
