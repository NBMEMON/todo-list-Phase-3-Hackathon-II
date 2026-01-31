import logging
import sys
from datetime import datetime
from typing import Any, Dict


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("conversational_ai")
    logger.setLevel(getattr(logging, level.upper()))
    
    # Prevent adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Create file handler
    file_handler = logging.FileHandler("conversational_ai.log")
    file_handler.setLevel(getattr(logging, level.upper()))
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger


def log_operation(operation: str, user_id: str, details: Dict[str, Any] = None, logger: logging.Logger = None):
    """
    Log an operation performed by the system.
    
    Args:
        operation: Type of operation being performed
        user_id: ID of the user performing the operation
        details: Additional details about the operation
        logger: Logger instance to use (optional)
    """
    if logger is None:
        logger = setup_logging()
    
    log_entry = {
        "operation": operation,
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "details": details or {}
    }
    
    logger.info(f"OPERATION: {log_entry}")


def log_api_call(endpoint: str, method: str, user_id: str, request_data: Dict[str, Any] = None, response_status: int = 200, logger: logging.Logger = None):
    """
    Log an API call to the system.
    
    Args:
        endpoint: API endpoint that was called
        method: HTTP method used
        user_id: ID of the user making the call
        request_data: Request payload (without sensitive information)
        response_status: HTTP response status
        logger: Logger instance to use (optional)
    """
    if logger is None:
        logger = setup_logging()
    
    log_entry = {
        "type": "api_call",
        "endpoint": endpoint,
        "method": method,
        "user_id": user_id,
        "request_size": len(str(request_data)) if request_data else 0,
        "response_status": response_status,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(f"API_CALL: {log_entry}")


def log_agent_execution(agent_name: str, user_id: str, input_data: Dict[str, Any], output_data: Dict[str, Any], execution_time_ms: float, logger: logging.Logger = None):
    """
    Log an agent execution.
    
    Args:
        agent_name: Name of the agent that executed
        user_id: ID of the user associated with the execution
        input_data: Input provided to the agent
        output_data: Output produced by the agent
        execution_time_ms: Time taken for execution in milliseconds
        logger: Logger instance to use (optional)
    """
    if logger is None:
        logger = setup_logging()
    
    log_entry = {
        "type": "agent_execution",
        "agent": agent_name,
        "user_id": user_id,
        "execution_time_ms": execution_time_ms,
        "input_size": len(str(input_data)),
        "output_size": len(str(output_data)),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.info(f"AGENT_EXECUTION: {log_entry}")


def log_error(error_type: str, user_id: str, error_message: str, context: Dict[str, Any] = None, logger: logging.Logger = None):
    """
    Log an error that occurred in the system.
    
    Args:
        error_type: Type/class of the error
        user_id: ID of the user associated with the error (if applicable)
        error_message: Error message
        context: Additional context about the error
        logger: Logger instance to use (optional)
    """
    if logger is None:
        logger = setup_logging()
    
    log_entry = {
        "type": "error",
        "error_type": error_type,
        "user_id": user_id,
        "error_message": error_message,
        "context": context or {},
        "timestamp": datetime.utcnow().isoformat()
    }
    
    logger.error(f"ERROR: {log_entry}")