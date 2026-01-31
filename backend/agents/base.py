from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """
    Abstract base class for all AI agents in the conversational todo system.
    Defines the common interface and shared functionality for all agents.
    """
    
    def __init__(self, name: str):
        """
        Initialize the agent with a name.
        
        Args:
            name: The name of the agent
        """
        self.name = name
    
    @abstractmethod
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the agent's primary function with the given context.
        
        Args:
            context: Dictionary containing execution context and parameters
            
        Returns:
            Dictionary containing the result of the execution
        """
        pass
    
    def log_execution(self, context: Dict[str, Any], result: Dict[str, Any]):
        """
        Log the execution details for debugging and monitoring.
        
        Args:
            context: The input context
            result: The execution result
        """
        print(f"[{self.name}] Executed with context: {context}, result: {result}")