from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
import uuid

from ..auth.middleware import get_current_user_from_token
from ..agents.main_orchestrator import process_conversation_turn
from ..utils.responses import create_success_response, create_error_response, handle_exception
from ..utils.logging import log_api_call, setup_logging

logger = setup_logging()

router = APIRouter(prefix="/chat", tags=["conversational-ai"])

@router.post("/process")
async def process_chat_message(
    request: Dict[str, Any],
    current_user: dict = Depends(get_current_user_from_token)
) -> Dict[str, Any]:
    """
    Process a user message in the conversational AI system.
    
    Args:
        request: Dictionary containing 'message' and optional 'session_id'
        current_user: Current authenticated user from JWT
        
    Returns:
        Dictionary with the AI response and session information
    """
    try:
        # Extract required fields
        user_message = request.get("message", "").strip()
        session_id = request.get("session_id") or str(uuid.uuid4())
        language = request.get("language", "auto")  # "en", "ur", or "auto"
        
        if not user_message:
            return create_error_response(
                error="EMPTY_MESSAGE",
                message="Message content is required",
                status_code=400
            )
        
        user_id = current_user.get("user_id")
        
        # Log the API call
        log_api_call(
            endpoint="/chat/process",
            method="POST",
            user_id=user_id,
            request_data={"message_length": len(user_message)},
            logger=logger
        )
        
        # Process the conversation turn
        result = await process_conversation_turn(
            user_input=user_message,
            user_id=user_id,
            session_id=session_id
        )
        
        # Prepare the response
        response_data = {
            "response": result.get("response", ""),
            "session_id": session_id,
            "language": language,  # Echo back the language preference
            "action_taken": result.get("action_taken", "unknown")
        }
        
        # Include task information if relevant
        if result.get("action_taken") in ["ADD_TASK", "VIEW_TASKS", "COMPLETE_TASK"]:
            response_data["task_info"] = result.get("entities", {})
        
        # Include task list if viewing tasks
        if result.get("action_taken") == "VIEW_TASKS":
            # This would come from the tool result if implemented
            pass
        
        return create_success_response(
            data=response_data,
            message="Message processed successfully"
        )
    
    except HTTPException as e:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in process_chat_message: {str(e)}")
        return handle_exception(e, "Error processing chat message")


@router.post("/start_session")
async def start_new_session(
    current_user: dict = Depends(get_current_user_from_token)
) -> Dict[str, Any]:
    """
    Start a new conversation session.
    
    Args:
        current_user: Current authenticated user from JWT
        
    Returns:
        Dictionary with the new session ID
    """
    try:
        user_id = current_user.get("user_id")
        session_id = str(uuid.uuid4())
        
        # Log the API call
        log_api_call(
            endpoint="/chat/start_session",
            method="POST",
            user_id=user_id,
            logger=logger
        )
        
        return create_success_response(
            data={
                "session_id": session_id,
                "message": "New session started"
            },
            message="New session started successfully"
        )
    
    except Exception as e:
        logger.error(f"Error in start_new_session: {str(e)}")
        return handle_exception(e, "Error starting new session")


@router.get("/session/{session_id}")
async def get_session_info(
    session_id: str,
    current_user: dict = Depends(get_current_user_from_token)
) -> Dict[str, Any]:
    """
    Get information about a specific session.
    
    Args:
        session_id: The session ID to retrieve info for
        current_user: Current authenticated user from JWT
        
    Returns:
        Dictionary with session information
    """
    try:
        user_id = current_user.get("user_id")
        
        # Log the API call
        log_api_call(
            endpoint=f"/chat/session/{session_id}",
            method="GET",
            user_id=user_id,
            logger=logger
        )
        
        # In a full implementation, we would retrieve session details from the database
        # For now, we'll just return basic session info
        return create_success_response(
            data={
                "session_id": session_id,
                "user_id": user_id,
                "status": "active",
                "message": "Session information retrieved"
            },
            message="Session information retrieved successfully"
        )
    
    except Exception as e:
        logger.error(f"Error in get_session_info: {str(e)}")
        return handle_exception(e, "Error retrieving session information")