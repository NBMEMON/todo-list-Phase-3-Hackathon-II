"""
MCP Tools for the AI-Powered Conversational Todo System
These tools provide a standardized interface for AI agents to perform operations
on the task management system, with proper authentication and validation.
"""

from typing import Dict, Any, Optional
from fastapi import HTTPException, Depends
from sqlmodel import Session
from datetime import datetime
import uuid

from ..models.task import Task
from ..database.session import get_session
from ..auth.middleware import get_current_user_from_token
from ..utils.responses import validate_and_extract_fields, create_success_response, create_error_response
from ..utils.logging import log_operation, setup_logging

logger = setup_logging()


class MCPTaskTools:
    """
    Collection of MCP tools for task management operations.
    Each method follows the MCP pattern with proper validation and authentication.
    """
    
    @staticmethod
    async def add_task(
        user_id: str,
        task_data: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to add a new task for the authenticated user.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            task_data: Dictionary containing task information
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to create tasks for this user"
                )
            
            # Validate required fields
            validated_data = validate_and_extract_fields(
                task_data,
                required_fields=["title"],
                optional_fields=["description", "priority", "due_date", "recurrence_pattern", "tags"]
            )
            
            # Create task object
            task_id = str(uuid.uuid4())
            db_task = Task(
                id=task_id,
                title=validated_data["title"],
                description=validated_data.get("description", ""),
                completed=validated_data.get("completed", False),
                priority=validated_data.get("priority", 3),
                due_date=validated_data.get("due_date"),
                recurrence_pattern=validated_data.get("recurrence_pattern"),
                user_id=user_id
            )
            
            # Add to session and commit
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            # Log the operation
            log_operation(
                operation="add_task",
                user_id=user_id,
                details={"task_id": task_id, "title": validated_data["title"]},
                logger=logger
            )
            
            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "title": db_task.title,
                    "message": "Task created successfully"
                },
                message="Task created successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in add_task: {str(e)}")
            return create_error_response(
                error="TASK_CREATION_FAILED",
                message=f"Failed to create task: {str(e)}"
            )

    @staticmethod
    async def add_task_with_validation(
        user_id: str,
        task_data: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to add a new task for the authenticated user with enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            task_data: Dictionary containing task information
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to create tasks for this user"
                )

            # Validate required fields
            validated_data = validate_and_extract_fields(
                task_data,
                required_fields=["title"],
                optional_fields=["description", "priority", "due_date", "recurrence_pattern", "tags"]
            )

            # Additional validation
            title = validated_data["title"].strip()
            if len(title) < 1 or len(title) > 200:
                raise HTTPException(
                    status_code=400,
                    detail="Task title must be between 1 and 200 characters"
                )

            priority = validated_data.get("priority", 3)
            if not isinstance(priority, int) or priority < 1 or priority > 5:
                raise HTTPException(
                    status_code=400,
                    detail="Priority must be an integer between 1 and 5"
                )

            # Validate due date if provided
            due_date_str = validated_data.get("due_date")
            if due_date_str:
                try:
                    from datetime import datetime
                    # Try to parse the date string
                    datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                    )

            # Validate recurrence pattern if provided
            recurrence_pattern = validated_data.get("recurrence_pattern")
            if recurrence_pattern:
                valid_patterns = ["daily", "weekly", "monthly", "custom"]
                if recurrence_pattern not in valid_patterns:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid recurrence pattern. Valid options: {valid_patterns}"
                    )

            # Create task object
            task_id = str(uuid.uuid4())
            db_task = Task(
                id=task_id,
                title=title,
                description=validated_data.get("description", ""),
                completed=validated_data.get("completed", False),
                priority=priority,
                due_date=due_date_str,
                recurrence_pattern=recurrence_pattern,
                user_id=user_id
            )

            # Add to session and commit
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Log the operation
            log_operation(
                operation="add_task_with_validation",
                user_id=user_id,
                details={"task_id": task_id, "title": title},
                logger=logger
            )

            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "title": db_task.title,
                    "message": "Task created successfully"
                },
                message="Task created successfully"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in add_task_with_validation: {str(e)}")
            return create_error_response(
                error="TASK_CREATION_FAILED",
                message=f"Failed to create task: {str(e)}"
            )
    
    @staticmethod
    async def list_tasks(
        user_id: str,
        filter_params: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to list tasks for the authenticated user with optional filtering.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            filter_params: Dictionary containing filter parameters
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status and list of tasks
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to access these tasks"
                )
            
            # Build query based on filters
            from sqlmodel import select
            query = select(Task).where(Task.user_id == user_id)
            
            # Apply status filter
            filter_status = filter_params.get("filter_status")
            if filter_status and filter_status != "all":
                is_completed = filter_status == "completed"
                query = query.where(Task.completed == is_completed)
            
            # Apply priority filter
            filter_priority = filter_params.get("filter_priority")
            if filter_priority is not None:
                query = query.where(Task.priority == filter_priority)
            
            # Apply search keyword filter
            search_keyword = filter_params.get("search_keyword")
            if search_keyword:
                search_pattern = f"%{search_keyword}%"
                query = query.where(Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern))
            
            # Execute query
            tasks = session.exec(query).all()
            
            # Log the operation
            log_operation(
                operation="list_tasks",
                user_id=user_id,
                details={
                    "filter_params": filter_params,
                    "task_count": len(tasks)
                },
                logger=logger
            )
            
            return create_success_response(
                data={
                    "tasks": [task.dict() for task in tasks],
                    "count": len(tasks),
                    "message": f"Retrieved {len(tasks)} tasks"
                },
                message=f"Retrieved {len(tasks)} tasks"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in list_tasks: {str(e)}")
            return create_error_response(
                error="TASK_LISTING_FAILED",
                message=f"Failed to list tasks: {str(e)}"
            )

    @staticmethod
    async def list_tasks_with_validation(
        user_id: str,
        filter_params: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to list tasks for the authenticated user with optional filtering and enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            filter_params: Dictionary containing filter parameters
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status and list of tasks
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to access these tasks"
                )

            # Validate filter parameters
            valid_statuses = ["completed", "pending", "all"]
            filter_status = filter_params.get("filter_status")
            if filter_status and filter_status not in valid_statuses:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid filter_status. Valid options: {valid_statuses}"
                )

            filter_priority = filter_params.get("filter_priority")
            if filter_priority is not None:
                if not isinstance(filter_priority, int) or filter_priority < 1 or filter_priority > 5:
                    raise HTTPException(
                        status_code=400,
                        detail="filter_priority must be an integer between 1 and 5"
                    )

            search_keyword = filter_params.get("search_keyword")
            if search_keyword and not isinstance(search_keyword, str):
                raise HTTPException(
                    status_code=400,
                    detail="search_keyword must be a string"
                )

            # Build query based on filters
            from sqlmodel import select
            query = select(Task).where(Task.user_id == user_id)

            # Apply status filter
            if filter_status and filter_status != "all":
                is_completed = filter_status == "completed"
                query = query.where(Task.completed == is_completed)

            # Apply priority filter
            if filter_priority is not None:
                query = query.where(Task.priority == filter_priority)

            # Apply search keyword filter
            if search_keyword:
                search_pattern = f"%{search_keyword}%"
                query = query.where(Task.title.ilike(search_pattern) | Task.description.ilike(search_pattern))

            # Execute query
            tasks = session.exec(query).all()

            # Log the operation
            log_operation(
                operation="list_tasks_with_validation",
                user_id=user_id,
                details={
                    "filter_params": filter_params,
                    "task_count": len(tasks)
                },
                logger=logger
            )

            return create_success_response(
                data={
                    "tasks": [task.dict() for task in tasks],
                    "count": len(tasks),
                    "message": f"Retrieved {len(tasks)} tasks"
                },
                message=f"Retrieved {len(tasks)} tasks"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in list_tasks_with_validation: {str(e)}")
            return create_error_response(
                error="TASK_LISTING_FAILED",
                message=f"Failed to list tasks: {str(e)}"
            )
    
    @staticmethod
    async def complete_task(
        user_id: str,
        task_id: str,
        completed: bool,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to mark a task as complete or incomplete.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            completed: Boolean indicating completion status
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )
            
            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()
            
            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )
            
            # Update completion status
            db_task.completed = completed
            db_task.updated_at = datetime.utcnow()
            
            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            # Log the operation
            log_operation(
                operation="complete_task",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "completed": completed
                },
                logger=logger
            )
            
            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "completed": db_task.completed,
                    "message": f"Task marked as {'complete' if completed else 'incomplete'}"
                },
                message=f"Task marked as {'complete' if completed else 'incomplete'}"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in complete_task: {str(e)}")
            return create_error_response(
                error="TASK_COMPLETION_FAILED",
                message=f"Failed to update task completion: {str(e)}"
            )

    @staticmethod
    async def complete_task_with_validation(
        user_id: str,
        task_id: str,
        completed: bool,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to mark a task as complete or incomplete with enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            completed: Boolean indicating completion status
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )

            # Validate inputs
            if not task_id:
                raise HTTPException(
                    status_code=400,
                    detail="task_id is required"
                )

            if completed is None:
                raise HTTPException(
                    status_code=400,
                    detail="completed status is required"
                )

            if not isinstance(completed, bool):
                raise HTTPException(
                    status_code=400,
                    detail="completed must be a boolean value"
                )

            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            # Update completion status
            db_task.completed = completed
            db_task.updated_at = datetime.utcnow()

            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Log the operation
            log_operation(
                operation="complete_task_with_validation",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "completed": completed
                },
                logger=logger
            )

            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "completed": db_task.completed,
                    "message": f"Task marked as {'complete' if completed else 'incomplete'}"
                },
                message=f"Task marked as {'complete' if completed else 'incomplete'}"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in complete_task_with_validation: {str(e)}")
            return create_error_response(
                error="TASK_COMPLETION_FAILED",
                message=f"Failed to update task completion: {str(e)}"
            )
    
    @staticmethod
    async def update_task(
        user_id: str,
        task_id: str,
        update_data: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to update task details.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            update_data: Dictionary containing fields to update
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )
            
            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()
            
            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )
            
            # Update the task with the provided fields
            for field, value in update_data.items():
                if hasattr(db_task, field):
                    setattr(db_task, field, value)
            
            # Update the timestamp
            db_task.updated_at = datetime.utcnow()
            
            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            # Log the operation
            log_operation(
                operation="update_task",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "updated_fields": list(update_data.keys())
                },
                logger=logger
            )
            
            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "message": "Task updated successfully"
                },
                message="Task updated successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_task: {str(e)}")
            return create_error_response(
                error="TASK_UPDATE_FAILED",
                message=f"Failed to update task: {str(e)}"
            )

    @staticmethod
    async def update_task_with_validation(
        user_id: str,
        task_id: str,
        update_data: Dict[str, Any],
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to update task details with enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            update_data: Dictionary containing fields to update
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )

            # Validate inputs
            if not task_id:
                raise HTTPException(
                    status_code=400,
                    detail="task_id is required"
                )

            if not update_data:
                raise HTTPException(
                    status_code=400,
                    detail="At least one field must be provided for update"
                )

            # Validate update data
            allowed_fields = {"title", "description", "priority", "due_date", "recurrence_pattern", "completed"}
            invalid_fields = set(update_data.keys()) - allowed_fields
            if invalid_fields:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid fields for update: {invalid_fields}"
                )

            # Validate individual fields
            if "title" in update_data:
                title = update_data["title"]
                if not isinstance(title, str) or len(title) < 1 or len(title) > 200:
                    raise HTTPException(
                        status_code=400,
                        detail="Task title must be a string between 1 and 200 characters"
                    )

            if "priority" in update_data:
                priority = update_data["priority"]
                if not isinstance(priority, int) or priority < 1 or priority > 5:
                    raise HTTPException(
                        status_code=400,
                        detail="Priority must be an integer between 1 and 5"
                    )

            if "due_date" in update_data:
                due_date_str = update_data["due_date"]
                if due_date_str:  # Allow null/empty values
                    try:
                        from datetime import datetime
                        # Try to parse the date string
                        datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                    except ValueError:
                        raise HTTPException(
                            status_code=400,
                            detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS.sssZ)"
                        )

            if "recurrence_pattern" in update_data:
                pattern = update_data["recurrence_pattern"]
                if pattern:  # Allow null/empty values
                    valid_patterns = ["daily", "weekly", "monthly", "custom"]
                    if pattern not in valid_patterns:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Invalid recurrence pattern. Valid options: {valid_patterns}"
                        )

            if "completed" in update_data:
                completed = update_data["completed"]
                if not isinstance(completed, bool):
                    raise HTTPException(
                        status_code=400,
                        detail="completed must be a boolean value"
                    )

            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            # Update the task with the provided fields
            for field, value in update_data.items():
                if hasattr(db_task, field):
                    setattr(db_task, field, value)

            # Update the timestamp
            db_task.updated_at = datetime.utcnow()

            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Log the operation
            log_operation(
                operation="update_task_with_validation",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "updated_fields": list(update_data.keys())
                },
                logger=logger
            )

            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "message": "Task updated successfully"
                },
                message="Task updated successfully"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in update_task_with_validation: {str(e)}")
            return create_error_response(
                error="TASK_UPDATE_FAILED",
                message=f"Failed to update task: {str(e)}"
            )
    
    @staticmethod
    async def delete_task(
        user_id: str,
        task_id: str,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to delete a task.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to delete
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to delete this task"
                )
            
            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()
            
            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )
            
            # Delete the task
            session.delete(db_task)
            session.commit()
            
            # Log the operation
            log_operation(
                operation="delete_task",
                user_id=user_id,
                details={"task_id": task_id},
                logger=logger
            )
            
            return create_success_response(
                data={
                    "task_id": task_id,
                    "message": "Task deleted successfully"
                },
                message="Task deleted successfully"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_task: {str(e)}")
            return create_error_response(
                error="TASK_DELETION_FAILED",
                message=f"Failed to delete task: {str(e)}"
            )

    @staticmethod
    async def delete_task_with_validation(
        user_id: str,
        task_id: str,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to delete a task with enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to delete
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to delete this task"
                )

            # Validate inputs
            if not task_id:
                raise HTTPException(
                    status_code=400,
                    detail="task_id is required"
                )

            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            # Delete the task
            session.delete(db_task)
            session.commit()

            # Log the operation
            log_operation(
                operation="delete_task_with_validation",
                user_id=user_id,
                details={"task_id": task_id},
                logger=logger
            )

            return create_success_response(
                data={
                    "task_id": task_id,
                    "message": "Task deleted successfully"
                },
                message="Task deleted successfully"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in delete_task_with_validation: {str(e)}")
            return create_error_response(
                error="TASK_DELETION_FAILED",
                message=f"Failed to delete task: {str(e)}"
            )
    
    @staticmethod
    async def set_recurring(
        user_id: str,
        task_id: str,
        pattern: str,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to set a recurring pattern for a task.
        
        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            pattern: Recurrence pattern (daily, weekly, monthly)
            session: Database session
            current_user: Current authenticated user from JWT
            
        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )
            
            # Validate recurrence pattern
            valid_patterns = ["daily", "weekly", "monthly"]
            if pattern not in valid_patterns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid recurrence pattern. Valid options: {valid_patterns}"
                )
            
            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()
            
            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )
            
            # Update recurrence pattern
            db_task.recurrence_pattern = pattern
            db_task.updated_at = datetime.utcnow()
            
            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)
            
            # Log the operation
            log_operation(
                operation="set_recurring",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "pattern": pattern
                },
                logger=logger
            )
            
            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "message": f"Recurrence pattern set to {pattern}"
                },
                message=f"Recurrence pattern set to {pattern}"
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in set_recurring: {str(e)}")
            return create_error_response(
                error="RECURRING_SET_FAILED",
                message=f"Failed to set recurring pattern: {str(e)}"
            )

    @staticmethod
    async def set_recurring_with_validation(
        user_id: str,
        task_id: str,
        pattern: str,
        session: Session = Depends(get_session),
        current_user: dict = Depends(get_current_user_from_token)
    ) -> Dict[str, Any]:
        """
        MCP tool to set a recurring pattern for a task with enhanced validation.

        Args:
            user_id: ID of the user (should match authenticated user)
            task_id: ID of the task to update
            pattern: Recurrence pattern (daily, weekly, monthly)
            session: Database session
            current_user: Current authenticated user from JWT

        Returns:
            Dictionary with success status and task information
        """
        try:
            # Verify that the requested user_id matches the authenticated user
            if current_user.get("user_id") != user_id:
                raise HTTPException(
                    status_code=403,
                    detail="Not authorized to update this task"
                )

            # Validate inputs
            if not task_id:
                raise HTTPException(
                    status_code=400,
                    detail="task_id is required"
                )

            if not pattern:
                raise HTTPException(
                    status_code=400,
                    detail="recurrence pattern is required"
                )

            # Validate recurrence pattern
            valid_patterns = ["daily", "weekly", "monthly", "custom"]
            if pattern not in valid_patterns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid recurrence pattern. Valid options: {valid_patterns}"
                )

            # Get the task
            from sqlmodel import select
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            db_task = session.exec(statement).first()

            if not db_task:
                raise HTTPException(
                    status_code=404,
                    detail="Task not found"
                )

            # Update recurrence pattern
            db_task.recurrence_pattern = pattern
            db_task.updated_at = datetime.utcnow()

            # Commit changes
            session.add(db_task)
            session.commit()
            session.refresh(db_task)

            # Log the operation
            log_operation(
                operation="set_recurring_with_validation",
                user_id=user_id,
                details={
                    "task_id": task_id,
                    "pattern": pattern
                },
                logger=logger
            )

            return create_success_response(
                data={
                    "task_id": db_task.id,
                    "recurrence_pattern": db_task.recurrence_pattern,
                    "message": f"Recurrence pattern set to {pattern}"
                },
                message=f"Recurrence pattern set to {pattern}"
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in set_recurring_with_validation: {str(e)}")
            return create_error_response(
                error="RECURRING_SET_FAILED",
                message=f"Failed to set recurring pattern: {str(e)}"
            )