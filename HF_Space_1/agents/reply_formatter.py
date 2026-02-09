from typing import Dict, Any
from .base import BaseAgent
from ..utils.logging import setup_logging

logger = setup_logging()


class ReplyFormatterAgent(BaseAgent):
    """
    Agent responsible for formatting responses from MCP tools into natural language
    with appropriate emojis and user-friendly messaging.
    """
    
    def __init__(self):
        super().__init__("ReplyFormatterAgent")
        
        # Emojis for different types of responses
        self.emojis = {
            "success": "✅",
            "error": "❌",
            "warning": "⚠️",
            "info": "ℹ️",
            "task": "📝",
            "complete": "✅",
            "incomplete": "⏳",
            "add": "➕",
            "delete": "🗑️",
            "update": "✏️",
            "list": "📋",
            "recurring": "🔄"
        }
        
        # Response templates
        self.response_templates_en = {
            "add_task_success": "{emoji} {title} has been added to your tasks!",
            "add_task_error": "{emoji} Sorry, I couldn't add that task: {message}",
            "list_tasks_empty": "{emoji} You don't have any tasks yet. Add one by saying 'Add a task to ...'",
            "list_tasks_single": "{emoji} You have 1 task: {task_info}",
            "list_tasks_multiple": "{emoji} You have {count} tasks: {task_list}",
            "complete_task_success": "{emoji} Task '{title}' has been marked as complete!",
            "complete_task_error": "{emoji} Sorry, I couldn't mark that task as complete: {message}",
            "update_task_success": "{emoji} Task has been updated!",
            "update_task_error": "{emoji} Sorry, I couldn't update that task: {message}",
            "delete_task_success": "{emoji} Task has been deleted!",
            "delete_task_error": "{emoji} Sorry, I couldn't delete that task: {message}",
            "set_recurring_success": "{emoji} Task will repeat {pattern}!",
            "set_recurring_error": "{emoji} Sorry, I couldn't set the recurring pattern: {message}",
            "unknown_intent": "{emoji} I'm not sure what you mean. Could you try rephrasing?",
            "error_generic": "{emoji} Something went wrong: {message}",
            "clarification_needed": "{emoji} I need a bit more information. What task would you like to {action}?",
            "greeting": "Hello! I'm your AI assistant. You can ask me to add, update, or manage your tasks.",
            "help": "I can help you manage your tasks. Try saying: 'Add a task to buy groceries', 'Show my tasks', or 'Mark task as complete'."
        }

        # Urdu response templates
        self.response_templates_ur = {
            "add_task_success": "{emoji} آپ کے کاموں میں {title} شامل کر دیا گیا ہے!",
            "add_task_error": "{emoji} معذرت، میں وہ کام شامل نہیں کر سکا: {message}",
            "list_tasks_empty": "{emoji} آپ کے پاس ابھی تک کوئی کام نہیں ہے۔ کوئی کام شامل کرنے کے لیے کہیں 'کام شامل کریں ...'",
            "list_tasks_single": "{emoji} آپ کے پاس 1 کام ہے: {task_info}",
            "list_tasks_multiple": "{emoji} آپ کے پاس {count} کام ہیں: {task_list}",
            "complete_task_success": "{emoji} کام '{title}' مکمل کے بطور نشان زد کر دیا گیا ہے!",
            "complete_task_error": "{emoji} معذرت، میں وہ کام مکمل کے بطور نشان زد نہیں کر سکا: {message}",
            "update_task_success": "{emoji} کام کو اپ ڈیٹ کر دیا گیا ہے!",
            "update_task_error": "{emoji} معذرت، میں وہ کام اپ ڈیٹ نہیں کر سکا: {message}",
            "delete_task_success": "{emoji} کام حذف کر دیا گیا ہے!",
            "delete_task_error": "{emoji} معذرت، میں وہ کام حذف نہیں کر سکا: {message}",
            "set_recurring_success": "{emoji} کام {pattern} دہرایا جائے گا!",
            "set_recurring_error": "{emoji} معذرت، میں دہرائی کا پیٹرن سیٹ نہیں کر سکا: {message}",
            "unknown_intent": "{emoji} مجھے سمجھ نہیں آ رہی کہ آپ کیا کہنا چاہتے ہیں۔ کیا آپ دوبارہ بیان کر سکتے ہیں؟",
            "error_generic": "{emoji} کچھ غلط ہو گیا: {message}",
            "clarification_needed": "{emoji} مجھے مزید معلومات درکار ہیں۔ آپ کون سا کام {action} چاہتے ہیں؟",
            "greeting": "ہیلو! میں آپ کا AI اسسٹنٹ ہوں۔ آپ مجھ سے کاموں کو شامل، اپ ڈیٹ، یا منظم کرنے کے لیے کہہ سکتے ہیں۔",
            "help": "میں آپ کے کاموں کو منظم کرنے میں مدد کر سکتا ہوں۔ کہنے کی کوشش کریں: 'کام شامل کریں تاکہ خریداری کریں'، 'میرے کام دکھائیں'، یا 'کام کو مکمل کے بطور نشان لگائیں'۔"
        }

        # Roman Urdu response templates
        self.response_templates_rom_ur = {
            "add_task_success": "{emoji} Aap ke kam mein {title} shamil kar diya gaya hai!",
            "add_task_error": "{emoji} Maaf kijeye, main woh kam shamil nahi kar sakta: {message}",
            "list_tasks_empty": "{emoji} Aap ke pass abi tak koi kam nahi hai. Koi kam shamil karne ke liye kehien 'kam shamil karen ...'",
            "list_tasks_single": "{emoji} Aap ke pass 1 kam hai: {task_info}",
            "list_tasks_multiple": "{emoji} Aap ke pass {count} kams hain: {task_list}",
            "complete_task_success": "{emoji} Kam '{title}' mukammal ke tor par nishan zed kar diya gaya hai!",
            "complete_task_error": "{emoji} Maaf kijeye, main woh kam mukammal ke tor par nishan zed nahi kar sakta: {message}",
            "update_task_success": "{emoji} Kam ko update kar diya gaya hai!",
            "update_task_error": "{emoji} Maaf kijeye, main woh kam update nahi kar sakta: {message}",
            "delete_task_success": "{emoji} Kam delete kar diya gaya hai!",
            "delete_task_error": "{emoji} Maaf kijeye, main woh kam delete nahi kar sakta: {message}",
            "set_recurring_success": "{emoji} Kam {pattern} dohraaya jaye ga!",
            "set_recurring_error": "{emoji} Maaf kijeye, main dohraai ka pattern set nahi kar sakta: {message}",
            "unknown_intent": "{emoji} Mujhe samajh nahi aa rahi ke aap kya kehna chahte hain. Kya aap dobara bayan kar sakte hain?",
            "error_generic": "{emoji} Kuch ghalat ho gaya: {message}",
            "clarification_needed": "{emoji} Mujhe mazeed maloomat darkar hain. Aap kon sa kam {action} chahte hain?",
            "greeting": "Hello! Main aap ka AI assistant hun. Aap mujh se kamon ko shamil, update, ya munaasik karne ke liye keh sakte hain.",
            "help": "Main aap ke kamon ko munaasik karne mein madad kar sakta hun. Kehte hue koshsish karen: 'kam shamil karen taake khareedi karen', 'mere kam dikhayen', ya 'kam ko mukammal ke tor par nishan lagayen'."
        }
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format the response from an MCP tool into natural language.
        
        Args:
            context: Dictionary containing 'tool_result', 'intent', and other formatting parameters
            
        Returns:
            Dictionary with formatted response
        """
        tool_result = context.get("tool_result", {})
        intent = context.get("intent", "")
        entities = context.get("entities", {})
        original_input = context.get("original_input", "")
        
        # Format the response based on the tool result
        formatted_response = self._format_response(tool_result, intent, entities, original_input)
        
        # Log the execution
        self.log_execution(
            context={"intent": intent, "entities": entities},
            result={"response": formatted_response}
        )

        return {
            "response": formatted_response,
            "intent": intent,
            "entities": entities,
            "original_input": original_input
        }

    def _get_response_templates(self, language: str):
        """
        Get the appropriate response templates based on the language.

        Args:
            language: The language code ('en' for English, 'ur' for Urdu, 'rom_ur' for Roman Urdu)

        Returns:
            Dictionary of response templates for the specified language
        """
        if language == 'ur':
            return self.response_templates_ur
        elif language == 'rom_ur':
            return self.response_templates_rom_ur
        else:
            # Default to English
            return self.response_templates_en
    
    def _format_response(self, tool_result: Dict[str, Any], intent: str, entities: Dict[str, Any], original_input: str) -> str:
        """
        Format the response based on the tool result and intent.
        
        Args:
            tool_result: Result from the MCP tool execution
            intent: The original intent
            entities: Extracted entities
            original_input: Original user input
            
        Returns:
            Formatted response string
        """
        success = tool_result.get("success", False)
        message = tool_result.get("message", "")
        data = tool_result.get("data", {})
        error = tool_result.get("error", "")
        
        # Determine the emoji to use
        emoji = self.emojis.get("success" if success else "error", "ℹ️")

        # Get the language from context
        language = context.get("language", "en")

        # Select the appropriate template based on language
        templates = self._get_response_templates(language)

        if success:
            # Format success responses based on intent
            if intent == "ADD_TASK":
                title = data.get("title", entities.get("task_title", "the task"))
                return templates["add_task_success"].format(emoji=self.emojis["add"], title=title)
            
            elif intent == "VIEW_TASKS":
                tasks = data.get("tasks", [])
                count = data.get("count", len(tasks))
                
                if count == 0:
                    return self.response_templates["list_tasks_empty"].format(emoji=self.emojis["list"])
                elif count == 1:
                    task = tasks[0]
                    status_emoji = self.emojis["complete"] if task.get("completed") else self.emojis["incomplete"]
                    task_info = f"{status_emoji} {task.get('title', 'Untitled')}"
                    return self.response_templates["list_tasks_single"].format(emoji=self.emojis["list"], task_info=task_info)
                else:
                    task_items = []
                    for task in tasks[:5]:  # Limit to first 5 tasks for brevity
                        status_emoji = self.emojis["complete"] if task.get("completed") else self.emojis["incomplete"]
                        task_items.append(f"{status_emoji} {task.get('title', 'Untitled')}")
                    
                    if count > 5:
                        task_items.append(f"... and {count - 5} more")
                    
                    task_list = ", ".join(task_items)
                    return self.response_templates["list_tasks_multiple"].format(
                        emoji=self.emojis["list"],
                        count=count,
                        task_list=task_list
                    )
            
            elif intent == "COMPLETE_TASK":
                title = entities.get("task_title", "the task")
                return self.response_templates["complete_task_success"].format(emoji=self.emojis["complete"], title=title)
            
            elif intent == "UPDATE_TASK":
                return self.response_templates["update_task_success"].format(emoji=self.emojis["update"])
            
            elif intent == "DELETE_TASK":
                return self.response_templates["delete_task_success"].format(emoji=self.emojis["delete"])
            
            elif intent == "SET_RECURRING":
                pattern = entities.get("recurrence", "the pattern")
                return self.response_templates["set_recurring_success"].format(emoji=self.emojis["recurring"], pattern=pattern)
            
            else:
                # Generic success response
                return f"{emoji} {message}"
        
        else:
            # Format error responses
            if error == "MISSING_TASK_ID" or "task_id" in message.lower():
                action = self._infer_action_from_input(original_input)
                return self.response_templates["clarification_needed"].format(
                    emoji=self.emojis["info"],
                    action=action
                )

            elif error == "UNKNOWN_INTENT":
                return self.response_templates["unknown_intent"].format(emoji=self.emojis["warning"])

            elif error == "MISSING_TITLE":
                return f"{self.emojis['error']} {message}"

            else:
                # Use specific error template if available, otherwise generic
                error_template = f"{self.emojis['error']} {message}"
                return self.response_templates.get(f"{intent.lower()}_error", error_template).format(
                    emoji=self.emojis["error"],
                    message=message
                )
    
    def _infer_action_from_input(self, input_text: str) -> str:
        """
        Infer the intended action from the user's input.
        
        Args:
            input_text: The original user input
            
        Returns:
            The inferred action
        """
        input_lower = input_text.lower()
        
        if any(word in input_lower for word in ["complete", "finish", "done", "mark"]):
            return "complete"
        elif any(word in input_lower for word in ["update", "change", "modify", "edit"]):
            return "update"
        elif any(word in input_lower for word in ["delete", "remove", "kill", "trash"]):
            return "delete"
        elif any(word in input_lower for word in ["add", "create", "new"]):
            return "add"
        else:
            return "manage"


# Convenience function to format responses
async def format_response(tool_result: Dict[str, Any], intent: str, entities: Dict[str, Any], original_input: str = "") -> str:
    """
    Convenience function to format a response.
    
    Args:
        tool_result: Result from the MCP tool execution
        intent: The original intent
        entities: Extracted entities
        original_input: Original user input
        
    Returns:
        Formatted response string
    """
    agent = ReplyFormatterAgent()
    context = {
        "tool_result": tool_result,
        "intent": intent,
        "entities": entities,
        "original_input": original_input
    }
    result = await agent.execute(context)
    return result["response"]