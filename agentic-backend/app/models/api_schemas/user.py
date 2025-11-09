from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user model with common fields"""
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool = True

class UserCreate(UserBase):
    """Model for creating a new user"""
    password: Optional[str] = None  # Optional for dev dummy user

class UserUpdate(BaseModel):
    """Model for updating a user"""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Complete user model with ID and timestamps"""
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """User response model for API responses"""
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool = False

class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr

class LoginResponse(BaseModel):
    """Login response model"""
    user: UserResponse
    message: str

class ChangePasswordRequest(BaseModel):
    """Change password request model"""
    current_password: str
    new_password: str
    confirm_password: str

class ChangePasswordResponse(BaseModel):
    """Change password response model"""
    message: str
    success: bool
