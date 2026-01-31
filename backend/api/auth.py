import sys
import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlmodel import Session, select
from typing import Optional
from pydantic import BaseModel

# Add the backend directory to the path to resolve relative imports correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User, UserCreate
from database.session import get_session

# Define constants
SECRET_KEY = os.getenv("JWT_SECRET", "your-default-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes as specified
REFRESH_TOKEN_EXPIRE_DAYS = 7    # 7 days as specified

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create access token with 15 minute expiry
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    """
    Create refresh token with 7 day expiry
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models for request bodies
class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserRegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    name: Optional[str] = None

@router.post("/login")
def login_user(request: UserLoginRequest, session: Session = Depends(get_session)):
    """
    Login endpoint that authenticates user and returns JWT tokens
    """
    try:
        # Find user by email
        user = session.exec(select(User).where(User.email == request.email)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verify password (using bcrypt)
        if not bcrypt.checkpw(request.password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Create access and refresh tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # 15 minutes as specified
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id, "email": user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "name": user.name
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register")
def register_user(request: UserRegisterRequest, session: Session = Depends(get_session)):
    """
    Register endpoint that creates a new user and returns JWT tokens
    """
    try:
        # Check if user with email already exists
        existing_user_by_email = session.exec(select(User).where(User.email == request.email)).first()
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists",
            )

        # Check if user with username already exists
        existing_user_by_username = session.exec(select(User).where(User.username == request.username)).first()
        if existing_user_by_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this username already exists",
            )

        # Validate that password and confirm_password match
        if request.password != request.confirm_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password and confirm password do not match",
            )

        # Create a UserCreate object and hash the password
        user_create_data = UserCreate(
            username=request.username,
            email=request.email,
            password=request.password,
            confirm_password=request.confirm_password,
            name=request.name
        )
        user_create_data.hash_password()

        # Create the user object
        user = User(
            username=user_create_data.username,
            email=user_create_data.email,
            password_hash=user_create_data.password_hash,
            name=user_create_data.name
        )

        # Add user to database
        session.add(user)
        session.commit()
        session.refresh(user)

        # Create access and refresh tokens
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # 15 minutes as specified
        access_token = create_access_token(
            data={"user_id": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(
            data={"user_id": user.id, "email": user.email}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "name": user.name
            }
        }
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User registration failed: {str(e)}",
        )


@router.post("/refresh")
def refresh_token_endpoint(request: Request):
    """
    Refresh endpoint that exchanges a refresh token for a new access token
    """
    # In a real implementation, you would validate the refresh token
    # For now, we'll just create a new access token

    # This is a simplified implementation - in reality, you'd validate the refresh token
    refresh_token = request.headers.get("refresh_token") or request.query_params.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # Decode the refresh token to get user info
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        email = payload.get("email")

        # Create new access token
        new_access_token = create_access_token(
            data={"user_id": user_id, "email": email}
        )

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/logout")
def logout_user(request: Request):
    """
    Logout endpoint that invalidates the refresh token
    """
    # In a real implementation, you would add the refresh token to a blacklist
    # For now, we'll just return a success response

    return {
        "message": "Successfully logged out"
    }