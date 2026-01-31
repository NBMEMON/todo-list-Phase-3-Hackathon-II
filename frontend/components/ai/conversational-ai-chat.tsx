'use client';

import { useState, useRef, useEffect } from 'react';
import { useConversationalOrchestrator } from '@/lib/ai/conversational-orchestrator';
import { useAuth } from '@/contexts/AuthContext';
import { Task } from '@/lib/api';

interface MessageBubbleProps {
  message: {
    id: string;
    text: string;
    sender: 'user' | 'ai';
    timestamp: Date;
  };
}

const MessageBubble = ({ message }: MessageBubbleProps) => {
  return (
    <div className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 ${
          message.sender === 'user'
            ? 'bg-indigo-600 text-white rounded-br-none'
            : 'bg-slate-800 text-slate-200 rounded-bl-none'
        }`}
      >
        <div className="text-sm">{message.text}</div>
        <div className={`text-xs mt-1 ${message.sender === 'user' ? 'text-indigo-200' : 'text-slate-400'}`}>
          {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    </div>
  );
};

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

const ChatInput = ({ onSendMessage, disabled }: ChatInputProps) => {
  const [inputValue, setInputValue] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (inputValue.trim() && !disabled) {
      onSendMessage(inputValue.trim());
      setInputValue('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  const handleInput = () => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`;
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mt-4">
      <div className="flex gap-2">
        <textarea
          ref={textareaRef}
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            handleInput();
          }}
          onKeyDown={handleKeyDown}
          placeholder="Ask me to add, update, or manage your tasks..."
          disabled={disabled}
          className="flex-1 bg-slate-800 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
          rows={1}
        />
        <button
          type="submit"
          disabled={disabled || !inputValue.trim()}
          className="bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl px-4 py-3 font-medium disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Send
        </button>
      </div>
    </form>
  );
};

interface ConversationalAIChatProps {
  onTaskUpdate?: (task: Task) => void;
  onTaskCreated?: (task: Task) => void;
  onTaskDeleted?: (taskId: string) => void;
}

export const ConversationalAIChat = ({
  onTaskUpdate,
  onTaskCreated,
  onTaskDeleted
}: ConversationalAIChatProps) => {
  const { user } = useAuth();
  const {
    messages,
    isLoading,
    processUserMessage,
    clearConversation
  } = useConversationalOrchestrator({
    userId: user?.id || '',
    onTaskUpdate,
    onTaskCreated,
    onTaskDeleted
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!user) {
    return (
      <div className="text-center py-10">
        <p className="text-slate-400">Please log in to use the AI assistant</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">AI Assistant</h3>
        <button
          onClick={clearConversation}
          className="text-sm text-slate-400 hover:text-slate-200"
        >
          Clear chat
        </button>
      </div>
      
      <div className="flex-1 overflow-y-auto max-h-[400px] pr-2">
        {messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}
        {isLoading && (
          <div className="flex justify-start mb-4">
            <div className="bg-slate-800 text-slate-200 rounded-2xl rounded-bl-none px-4 py-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-slate-400 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-slate-400 animate-bounce delay-75"></div>
                <div className="w-2 h-2 rounded-full bg-slate-400 animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput onSendMessage={processUserMessage} disabled={isLoading} />
      
      <div className="mt-4 text-xs text-slate-500">
        <p>Examples: "Add a task to buy groceries", "Show my tasks", "Mark task as complete"</p>
      </div>
    </div>
  );
};