from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any
import json


class ConversationThread(SQLModel, table=True):
    """
    Represents a conversation thread between a user and the AI assistant.
    Stores the conversation history and context.
    """

    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)  # Foreign key to User
    session_id: str = Field(index=True)  # Unique session identifier
    messages: str = Field(default="[]")  # JSON string of message objects
    context: str = Field(default="{}")  # JSON string of conversation context
    language_preference: str = Field(default="auto")  # "en", "ur", or "auto"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str, language: str = "en"):
        """
        Add a message to the conversation thread.

        Args:
            role: "user" or "assistant"
            content: The message content
            language: The language of the message ("en" or "ur")
        """
        messages = json.loads(self.messages)
        message_obj = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat(),
            "language": language
        }
        messages.append(message_obj)
        self.messages = json.dumps(messages)
        self.updated_at = datetime.utcnow()

    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in the conversation thread.

        Returns:
            List of message dictionaries
        """
        return json.loads(self.messages)

    def set_context_value(self, key: str, value: Any):
        """
        Set a value in the conversation context.

        Args:
            key: The context key
            value: The value to set
        """
        context = json.loads(self.context)
        context[key] = value
        self.context = json.dumps(context)
        self.updated_at = datetime.utcnow()

    def get_context_value(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the conversation context.

        Args:
            key: The context key
            default: Default value if key doesn't exist

        Returns:
            The value associated with the key or default
        """
        context = json.loads(self.context)
        return context.get(key, default)

    def clear_context(self):
        """
        Clear the conversation context.
        """
        self.context = json.dumps({})
        self.updated_at = datetime.utcnow()

    def get_last_n_messages(self, n: int) -> List[Dict[str, Any]]:
        """
        Get the last n messages from the conversation thread.

        Args:
            n: Number of messages to retrieve

        Returns:
            List of the last n message dictionaries
        """
        messages = self.get_messages()
        return messages[-n:] if len(messages) >= n else messages

    def get_messages_by_role(self, role: str) -> List[Dict[str, Any]]:
        """
        Get all messages from a specific role in the conversation thread.

        Args:
            role: "user" or "assistant"

        Returns:
            List of message dictionaries from the specified role
        """
        messages = self.get_messages()
        return [msg for msg in messages if msg.get("role") == role]

    def get_messages_by_language(self, language: str) -> List[Dict[str, Any]]:
        """
        Get all messages in a specific language.

        Args:
            language: Language code ("en" or "ur")

        Returns:
            List of message dictionaries in the specified language
        """
        messages = self.get_messages()
        return [msg for msg in messages if msg.get("language") == language]