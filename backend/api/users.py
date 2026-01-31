from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Optional

from models.user import User, UserRead
from database.session import get_session
from auth.middleware import get_current_user_from_token

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=UserRead)
def get_current_user(
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get current user's profile information
    """
    user_id = current_user.get("user_id")
    
    # Get the user from the database
    statement = select(User).where(User.id == user_id)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user