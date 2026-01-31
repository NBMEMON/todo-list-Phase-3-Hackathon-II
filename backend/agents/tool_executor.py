from typing import Dict, Any
from .base import BaseAgent
from ..api.mcp_tools import MCPTaskTools
from ..utils.logging import setup_logging

logger = setup_logging()


class MCPToolExecutorAgent(BaseAgent):
    """
    Agent responsible for executing MCP tools based on parsed intents and entities.
    """
    
    def __init__(self):
        super().__init__("MCPToolExecutorAgent")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the appropriate MCP tool based on the intent and parameters.
        
        Args:
            context: Dictionary containing 'intent', 'entities', 'user_id', and other parameters
            
        Returns:
            Dictionary with the result of the MCP tool execution
        """
        intent = context.get("intent")
        entities = context.get("entities", {})
        user_id = context.get("user_id")
        
        if not intent or not user_id:
            return {
                "success": False,
                "error": "Missing intent or user_id in context",
                "message": "Unable to execute tool without intent and user identification"
            }
        
        # Map intent to the appropriate MCP tool
        try:
            if intent == "ADD_TASK":
                result = await self._execute_add_task(user_id, entities, context)
            elif intent == "VIEW_TASKS":
                result = await self._execute_view_tasks(user_id, entities, context)
            elif intent == "COMPLETE_TASK":
                result = await self._execute_complete_task(user_id, entities, context)
            elif intent == "UPDATE_TASK":
                result = await self._execute_update_task(user_id, entities, context)
            elif intent == "DELETE_TASK":
                result = await self._execute_delete_task(user_id, entities, context)
            elif intent == "SET_RECURRING":
                result = await self._execute_set_recurring(user_id, entities, context)
            else:
                result = {
                    "success": False,
                    "error": "UNKNOWN_INTENT",
                    "message": f"Unknown intent: {intent}"
                }
        except Exception as e:
            logger.error(f"Error executing MCP tool for intent {intent}: {str(e)}")
            result = {
                "success": False,
                "error": "EXECUTION_ERROR",
                "message": f"Error executing tool: {str(e)}"
            }
        
        # Log the execution
        self.log_execution(
            context={"intent": intent, "user_id": user_id, "entities": entities},
            result=result
        )
        
        return result
    
    async def _execute_add_task(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the add_task MCP tool.

        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context

        Returns:
            Result of the add_task operation
        """
        # Check if required entities are present
        if not entities.get("task_title"):
            return {
                "success": False,
                "error": "MISSING_TITLE",
                "message": "I couldn't find a task title in your message. Please specify what task you'd like to add."
            }

        # Prepare task data from entities
        task_data = {
            "title": entities.get("task_title", ""),
            "description": entities.get("task_description", ""),
            "priority": entities.get("priority", 3),
            "due_date": entities.get("due_date"),
            "recurrence_pattern": entities.get("recurrence")
        }

        # Remove empty values
        task_data = {k: v for k, v in task_data.items() if v is not None and v != ""}

        # Call the MCP tool
        return await MCPTaskTools.add_task(
            user_id=user_id,
            task_data=task_data
        )
    
    async def _execute_view_tasks(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the list_tasks MCP tool.
        
        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context
            
        Returns:
            Result of the list_tasks operation
        """
        # Prepare filter parameters from entities
        filter_params = {
            "filter_status": entities.get("status"),
            "filter_priority": entities.get("priority"),
            "search_keyword": entities.get("search_keyword", entities.get("task_title"))
        }
        
        # Remove empty values
        filter_params = {k: v for k, v in filter_params.items() if v is not None and v != ""}
        
        # Call the MCP tool
        return await MCPTaskTools.list_tasks(
            user_id=user_id,
            filter_params=filter_params
        )
    
    async def _execute_complete_task(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the complete_task MCP tool.
        
        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context
            
        Returns:
            Result of the complete_task operation
        """
        task_id = entities.get("task_id")
        
        if not task_id:
            # If no task ID is provided, we might need to look up by title
            if "task_title" in entities:
                # This would require additional logic to find the task by title
                # For now, return an error
                return {
                    "success": False,
                    "error": "MISSING_TASK_ID",
                    "message": "Task ID is required to complete a task"
                }
        
        # Call the MCP tool
        return await MCPTaskTools.complete_task(
            user_id=user_id,
            task_id=task_id,
            completed=True
        )
    
    async def _execute_update_task(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the update_task MCP tool.
        
        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context
            
        Returns:
            Result of the update_task operation
        """
        task_id = entities.get("task_id")
        
        if not task_id:
            return {
                "success": False,
                "error": "MISSING_TASK_ID",
                "message": "Task ID is required to update a task"
            }
        
        # Prepare update data from entities
        update_data = {
            "title": entities.get("task_title"),
            "description": entities.get("task_description"),
            "priority": entities.get("priority"),
            "due_date": entities.get("due_date"),
            "recurrence_pattern": entities.get("recurrence")
        }
        
        # Remove empty values
        update_data = {k: v for k, v in update_data.items() if v is not None and v != ""}
        
        # Call the MCP tool
        return await MCPTaskTools.update_task(
            user_id=user_id,
            task_id=task_id,
            update_data=update_data
        )
    
    async def _execute_delete_task(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the delete_task MCP tool.
        
        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context
            
        Returns:
            Result of the delete_task operation
        """
        task_id = entities.get("task_id")
        
        if not task_id:
            return {
                "success": False,
                "error": "MISSING_TASK_ID",
                "message": "Task ID is required to delete a task"
            }
        
        # Call the MCP tool
        return await MCPTaskTools.delete_task(
            user_id=user_id,
            task_id=task_id
        )
    
    async def _execute_set_recurring(self, user_id: str, entities: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the set_recurring MCP tool.
        
        Args:
            user_id: ID of the user
            entities: Dictionary of extracted entities
            context: Original context
            
        Returns:
            Result of the set_recurring operation
        """
        task_id = entities.get("task_id")
        pattern = entities.get("recurrence")
        
        if not task_id:
            return {
                "success": False,
                "error": "MISSING_TASK_ID",
                "message": "Task ID is required to set recurrence"
            }
        
        if not pattern:
            return {
                "success": False,
                "error": "MISSING_PATTERN",
                "message": "Recurrence pattern is required"
            }
        
        # Call the MCP tool
        return await MCPTaskTools.set_recurring(
            user_id=user_id,
            task_id=task_id,
            pattern=pattern
        )


# Convenience function to execute tools
async def execute_tool(intent: str, user_id: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to execute an MCP tool.
    
    Args:
        intent: The intent to execute
        user_id: The user ID
        entities: Extracted entities
        
    Returns:
        Result of the tool execution
    """
    agent = MCPToolExecutorAgent()
    context = {
        "intent": intent,
        "user_id": user_id,
        "entities": entities
    }
    return await agent.execute(context)