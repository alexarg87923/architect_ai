from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db, User as UserDB
from app.services.user_service import UserService
from app.models.agent import LoginRequest, UserResponse, User, LoginResponse, ChangePasswordRequest, ChangePasswordResponse
from typing import Dict

router = APIRouter()
user_service = UserService()

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Simple login endpoint for development
    In production, this would return JWT tokens
    """
    try:
        # Authenticate user
        user = user_service.authenticate_user(
            db, 
            email=login_data.email, 
            password=None  # No password for dev mode
        )
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # For development: return user data directly
        # In production: return JWT token
        return LoginResponse(
            message="Login successful",
            user=UserResponse(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                is_superuser=user.is_superuser
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    user_id: int,  # In production, this would come from JWT token
    db: Session = Depends(get_db)
):
    """
    Get current user information
    For development, user_id is passed as query parameter
    """
    try:
        user = user_service.get_user_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,  
            created_at=user.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user: {str(e)}"
        )

@router.post("/change-password", response_model=ChangePasswordResponse)
async def change_password(
    user_id: int,
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Change user password
    For development, user_id is passed as query parameter
    """
    try:
        # Validate passwords match
        if password_data.new_password != password_data.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password and confirm password do not match"
            )
        
        # Validate password length
        if len(password_data.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 6 characters long"
            )
        
        # Validate current password is provided
        if not password_data.current_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is required"
            )
        
        # Get user from database directly to access password_hash
        db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not user_service.verify_password(password_data.current_password, db_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        success = user_service.update_password(db, user_id, password_data.new_password)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update password"
            )
        
        return ChangePasswordResponse(
            message="Password changed successfully",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to change password: {str(e)}"
        )
