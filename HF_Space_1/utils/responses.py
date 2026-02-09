from typing import Any, Dict, Optional
from fastapi import HTTPException


def create_success_response(data: Optional[Any] = None, message: str = "Success", status_code: int = 200) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Optional data to include in the response
        message: Success message
        status_code: HTTP status code (default 200)
        
    Returns:
        Dictionary with standardized success response format
    """
    response = {
        "success": True,
        "message": message,
        "status_code": status_code
    }
    
    if data is not None:
        response["data"] = data
        
    return response


def create_error_response(error: str, message: str = "Error occurred", status_code: int = 400) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        error: Error type or code
        message: Error message
        status_code: HTTP status code (default 400)
        
    Returns:
        Dictionary with standardized error response format
    """
    return {
        "success": False,
        "error": error,
        "message": message,
        "status_code": status_code
    }


def handle_exception(exception: Exception, default_message: str = "An error occurred") -> Dict[str, Any]:
    """
    Handle an exception and return a standardized error response.
    
    Args:
        exception: The exception that occurred
        default_message: Default message if exception doesn't have a message
        
    Returns:
        Dictionary with standardized error response format
    """
    if hasattr(exception, 'detail'):
        message = str(exception.detail)
    elif str(exception):
        message = str(exception)
    else:
        message = default_message
    
    return create_error_response(
        error=type(exception).__name__,
        message=message,
        status_code=getattr(exception, 'status_code', 500) if hasattr(exception, 'status_code') else 500
    )


def validate_and_extract_fields(request_data: Dict[str, Any], required_fields: list, optional_fields: Optional[list] = None) -> Dict[str, Any]:
    """
    Validate required fields in request data and extract optional fields.
    
    Args:
        request_data: Incoming request data
        required_fields: List of required field names
        optional_fields: List of optional field names
        
    Returns:
        Dictionary with validated and extracted fields
        
    Raises:
        HTTPException: If required fields are missing
    """
    if optional_fields is None:
        optional_fields = []
    
    # Check for required fields
    for field in required_fields:
        if field not in request_data or request_data[field] is None:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    # Extract required fields
    result = {field: request_data[field] for field in required_fields}
    
    # Extract optional fields if they exist
    for field in optional_fields:
        if field in request_data and request_data[field] is not None:
            result[field] = request_data[field]
    
    return result