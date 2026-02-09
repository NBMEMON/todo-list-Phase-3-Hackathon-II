from typing import Dict, Any
from .base import BaseAgent
from .intent_parser import IntentParserAgent, parse_intent
from .tool_executor import MCPToolExecutorAgent, execute_tool
from .reply_formatter import ReplyFormatterAgent, format_response
from ..models.conversation_thread import ConversationThread
from ..database.session import get_session
from ..utils.logging import setup_logging

logger = setup_logging()


class MainOrchestratorAgent(BaseAgent):
    """
    Main orchestrator agent that coordinates the overall conversation flow
    between the intent parser, tool executor, and reply formatter.
    """
    
    def __init__(self):
        super().__init__("MainOrchestratorAgent")
        self.intent_parser = IntentParserAgent()
        self.tool_executor = MCPToolExecutorAgent()
        self.reply_formatter = ReplyFormatterAgent()
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the full conversation flow: parse intent, execute tool, format response.
        
        Args:
            context: Dictionary containing 'user_input', 'user_id', and other context
            
        Returns:
            Dictionary with the final response and execution details
        """
        user_input = context.get("user_input", "")
        user_id = context.get("user_id", "")
        session_id = context.get("session_id", "")
        
        if not user_input:
            return {
                "success": False,
                "response": "I didn't receive any input. Could you please say something?",
                "action_taken": "none"
            }
        
        if not user_id:
            return {
                "success": False,
                "response": "User authentication required. Please log in.",
                "action_taken": "auth_required"
            }

        try:
            # Step 1: Parse intent and extract entities
            intent_result = await self.intent_parser.execute({"user_input": user_input})
            intent = intent_result["intent"]
            entities = intent_result["entities"]
            confidence = intent_result["confidence"]
            language = intent_result.get("language", "en")  # Get detected language

            # Log the intent parsing
            logger.info(f"Intent parsed: {intent} with confidence {confidence} for user {user_id}")

            # If intent is unknown or confidence is low, provide a helpful response
            if intent == "UNKNOWN" or confidence < 0.5:
                response = await self._handle_unknown_intent(user_input)
                return {
                    "success": True,
                    "response": response,
                    "action_taken": "unknown_intent_handled",
                    "intent": intent,
                    "confidence": confidence
                }

            # Step 2: Execute the appropriate tool
            tool_result = await self.tool_executor.execute({
                "intent": intent,
                "user_id": user_id,
                "entities": entities,
                "original_input": user_input
            })

            # Step 3: Format the response
            formatted_response = await self.reply_formatter.execute({
                "tool_result": tool_result,
                "intent": intent,
                "entities": entities,
                "original_input": user_input,
                "language": language  # Pass language to formatter
            })

            response_text = formatted_response["response"]

            # Log the execution
            self.log_execution(
                context={
                    "user_id": user_id,
                    "session_id": session_id,
                    "user_input": user_input,
                    "intent": intent,
                    "confidence": confidence
                },
                result={
                    "response": response_text,
                    "tool_success": tool_result.get("success", False),
                    "action_taken": intent
                }
            )

            return {
                "success": True,
                "response": response_text,
                "action_taken": intent,
                "intent": intent,
                "confidence": confidence,
                "entities": entities,
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Error in MainOrchestratorAgent execution: {str(e)}")
            return {
                "success": False,
                "response": "Sorry, I encountered an error processing your request. Could you please try again?",
                "action_taken": "error",
                "error": str(e)
            }
    
    async def _handle_unknown_intent(self, user_input: str) -> str:
        """
        Handle cases where the intent is unknown or confidence is low.
        
        Args:
            user_input: The user's input
            
        Returns:
            Formatted response for unknown intent
        """
        # Check if the input is a greeting
        greeting_keywords = ["hello", "hi", "hey", "greetings", "morning", "afternoon", "evening"]
        if any(keyword in user_input.lower() for keyword in greeting_keywords):
            return "Hello! I'm your AI assistant. You can ask me to add, update, or manage your tasks. Try saying 'Add a task to buy groceries'"
        
        # Check if the input is asking for help
        help_keywords = ["help", "what can you do", "how do i", "instructions", "guide"]
        if any(keyword in user_input.lower() for keyword in help_keywords):
            return "I can help you manage your tasks. Try saying: 'Add a task to buy groceries', 'Show my tasks', or 'Mark task as complete'."
        
        # Default response for unknown intent
        return "I'm not sure what you mean. Could you try rephrasing? You can ask me to add, update, or manage your tasks."
    
    async def process_conversation_turn(self, user_input: str, user_id: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a single turn in a conversation, maintaining context.
        
        Args:
            user_input: The user's input message
            user_id: The ID of the user
            session_id: Optional session ID for maintaining conversation context
            
        Returns:
            Dictionary with the response and conversation details
        """
        context = {
            "user_input": user_input,
            "user_id": user_id,
            "session_id": session_id
        }
        
        return await self.execute(context)


# Convenience function to process a conversation turn
async def process_conversation_turn(user_input: str, user_id: str, session_id: str = None) -> Dict[str, Any]:
    """
    Convenience function to process a conversation turn.
    
    Args:
        user_input: The user's input message
        user_id: The ID of the user
        session_id: Optional session ID for maintaining conversation context
        
    Returns:
        Dictionary with the response and conversation details
    """
    agent = MainOrchestratorAgent()
    return await agent.process_conversation_turn(user_input, user_id, session_id)