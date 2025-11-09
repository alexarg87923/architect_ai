from sqlalchemy.orm import Session
from app.core.database import User as UserDB
from app.models.agent import User, UserCreate, UserResponse, LoginRequest
from typing import Optional
from datetime import datetime
import hashlib

class UserService:
    """Service for handling user operations"""
    
    def create_user(self, db: Session, user_create: UserCreate) -> User:
        """Create a new user"""
        # Simple hash for development (use bcrypt in production)
        password_hash = hashlib.sha256(user_create.password.encode()).hexdigest() if user_create.password else None
        
        db_user = UserDB(
            email=user_create.email,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            password_hash=password_hash,
            is_active=user_create.is_active
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        db_user = db.query(UserDB).filter(UserDB.email == email).first()
        if not db_user:
            return None
            
        return User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            return None
            
        return User(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at
        )
    
    def authenticate_user(self, db: Session, email: str, password: Optional[str] = None) -> Optional[User]:
        """Authenticate user (simplified for development)"""
        user = self.get_user_by_email(db, email)
        if not user or not user.is_active:
            return None
        
        # For development: if no password provided, just return user
        # In production: verify password hash
        if password is None:
            return user
            
        # Simple password check for development
        db_user = db.query(UserDB).filter(UserDB.email == email).first()
        if db_user and db_user.password_hash:
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            if password_hash == db_user.password_hash:
                return user
        
        return None
    
    def user_exists(self, db: Session, email: str) -> bool:
        """Check if user exists by email"""
        return db.query(UserDB).filter(UserDB.email == email).first() is not None
    
    def user_exists_by_id(self, db: Session, user_id: int) -> bool:
        """Check if user exists by ID"""
        return db.query(UserDB).filter(UserDB.id == user_id).first() is not None

    def update_password(self, db: Session, user_id: int, new_password: str) -> bool:
        """Update user password"""
        try:
            db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
            if not db_user:
                return False
            
            # Hash the new password
            password_hash = hashlib.sha256(new_password.encode()).hexdigest()
            
            # Update password hash
            db_user.password_hash = password_hash
            db_user.updated_at = datetime.utcnow()
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            print(f"Error updating password: {e}")
            return False

    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify a password against its stored hash"""
        try:
            # Hash the provided password
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Compare with stored hash
            return password_hash == stored_hash
            
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False
