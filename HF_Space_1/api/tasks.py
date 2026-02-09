import sys
import os
# Add the backend directory to the path to resolve relative imports correctly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from models.task import Task, TaskCreate, TaskRead, TaskUpdate
from database.session import get_session
from auth.middleware import get_current_user_from_token

router = APIRouter(tags=["tasks"])

@router.get("/{user_id}/tasks", response_model=List[TaskRead])
def get_tasks(
    user_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get all tasks for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access these tasks"
        )

    # Query tasks for the user
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskRead)
def create_task(
    user_id: str,
    task: TaskCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Create a new task for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create tasks for this user"
        )

    # Create task object
    db_task = Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        user_id=user_id
    )

    # Add to session and commit
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def get_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Get a specific task by ID for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this task"
        )

    # Get the task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return db_task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead)
def update_task(
    user_id: str,
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Update a specific task by ID for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Get the task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the provided fields
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    # Update the timestamp
    db_task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


from pydantic import BaseModel

class TaskCompletionUpdate(BaseModel):
    completed: bool

@router.patch("/{user_id}/tasks/{task_id}/complete")
def toggle_task_completion(
    user_id: str,
    task_id: str,
    task_update: TaskCompletionUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Toggle task completion status for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this task"
        )

    # Get the task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update completion status
    db_task.completed = task_update.completed
    db_task.updated_at = datetime.utcnow()

    # Commit changes
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return {"id": db_task.id, "completed": db_task.completed, "updated_at": db_task.updated_at}


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: str,
    session: Session = Depends(get_session),
    current_user: dict = Depends(get_current_user_from_token)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    # Verify that the requested user_id matches the authenticated user
    if current_user.get("user_id") != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this task"
        )

    # Get the task
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    session.delete(db_task)
    session.commit()

    return {"message": "Task deleted successfully"}