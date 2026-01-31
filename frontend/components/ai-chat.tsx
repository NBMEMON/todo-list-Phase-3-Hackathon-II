import React, { useState, useRef, useEffect } from 'react';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface AIChatProps {
  userId: string;
  sessionId?: string;
  onNewMessage?: (message: Message) => void;
  onSessionChange?: (sessionId: string) => void;
}

const AIChat: React.FC<AIChatProps> = ({ userId, sessionId: propSessionId, onNewMessage, onSessionChange }) => {
  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState(propSessionId || '');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when new messages arrive
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Function to send a message to the backend
  const sendMessage = async (text: string) => {
    if (!text.trim() || isLoading) return;

    // Add user message to the chat
    const userMessage: Message = {
      id: Date.now().toString(),
      text,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      // Call the backend API to process the message
      const response = await fetch('/api/chat/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // Assuming JWT token is stored in localStorage
        },
        body: JSON.stringify({
          message: text,
          session_id: currentSessionId,
          language: 'en' // Default to English, could be changed based on user preference
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Update session ID if it changed
      if (data.data && data.data.session_id && data.data.session_id !== currentSessionId) {
        setCurrentSessionId(data.data.session_id);
        onSessionChange?.(data.data.session_id);
      }

      // Add AI response to the chat
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: data.data.response,
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
      onNewMessage?.(aiMessage);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message to the chat
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "Sorry, I encountered an error processing your request. Please try again.",
        sender: 'ai',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputText);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(inputText);
    }
  };

  const startNewSession = async () => {
    try {
      const response = await fetch('/api/chat/start_session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const newSessionId = data.data.session_id;
      
      setCurrentSessionId(newSessionId);
      onSessionChange?.(newSessionId);
      setMessages([]); // Clear the chat for the new session
    } catch (error) {
      console.error('Error starting new session:', error);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-50 rounded-lg shadow-md">
      <div className="p-4 bg-indigo-600 text-white rounded-t-lg">
        <div className="flex justify-between items-center">
          <h3 className="text-lg font-semibold">AI Assistant</h3>
          <button
            onClick={startNewSession}
            className="px-3 py-1 bg-white text-indigo-600 rounded-md text-sm font-medium hover:bg-gray-100 transition-colors"
          >
            New Chat
          </button>
        </div>
        {currentSessionId && (
          <p className="text-xs opacity-80 mt-1">Session: {currentSessionId.substring(0, 8)}...</p>
        )}
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[400px]" style={{ minHeight: '300px' }}>
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            <p>Start a conversation with the AI assistant...</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-2 ${
                  message.sender === 'user'
                    ? 'bg-indigo-500 text-white rounded-br-none'
                    : 'bg-white text-gray-800 rounded-bl-none border border-gray-200'
                }`}
              >
                <div className="text-sm">{message.text}</div>
                <div
                  className={`text-xs mt-1 ${
                    message.sender === 'user' ? 'text-indigo-200' : 'text-gray-500'
                  }`}
                >
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white text-gray-800 rounded-2xl rounded-bl-none px-4 py-2 border border-gray-200">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-75"></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200">
        <div className="flex gap-2">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to add, update, or manage your tasks..."
            className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
            rows={2}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputText.trim() || isLoading}
            className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Try: "Add a task to buy groceries", "Show my tasks", "Mark task as complete"
        </div>
      </form>
    </div>
  );
};

export default AIChat;