from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Database Models
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True, index=True)  # Link to project
    project_name = Column(String, nullable=True)
    specifications = Column(JSON, nullable=True)  # Store project specs as JSON
    current_phase = Column(String, default="discovery")  # discovery, confirmation, generation
    is_specification_complete = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    project = relationship("Project", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
    roadmaps = relationship("Roadmap", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    action_type = Column(String, nullable=True)  # "chat", "edit", "expand"
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Direct user association
    roadmap_data = Column(JSON)  # Store the full roadmap JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="roadmaps")
    conversation = relationship("Conversation", back_populates="roadmaps")

# User table
# Project table
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="draft")  # draft, active, completed, archived
    roadmap_data = Column(JSON, nullable=True)  # Store roadmap nodes as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    conversations = relationship("Conversation", back_populates="project")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)
    task_type = Column(String, nullable=False)  # "daily-todos" or "your-ideas"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    archive = Column(Boolean,default=False)
    
    # Relationships
    project = relationship("Project", back_populates="tasks")

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    feedback_type = Column(String, nullable=False)  # "general", "bug", "feature", "improvement"
    message = Column(Text, nullable=False)
    status = Column(String, default="pending")  # "pending", "reviewed", "resolved", "closed"
    admin_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="feedback")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    password_hash = Column(String, nullable=True)  # Nullable for dev dummy user
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False) 
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user")
    roadmaps = relationship("Roadmap", back_populates="user")
    projects = relationship("Project", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
