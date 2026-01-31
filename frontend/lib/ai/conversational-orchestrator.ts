'use client';

import { useState, useEffect, useRef } from 'react';
import { IntentParserAgent, IntentType } from '@/lib/ai/intent-parser';
import { MCPToolExecutorPhaseIII, ToolRequest } from '@/lib/ai/mcp-tool-executor';
import { ReplyFormatter } from '@/lib/ai/reply-formatter';
import { EnhancedIntentClassifier } from '@/lib/ai/cohere-integration';
import { Task } from '@/lib/api';

interface UserMessage {
  id: string;
  text: string;
  sender: 'user' | 'ai';
  timestamp: Date;
}

interface ConversationalOrchestratorProps {
  userId: string;
  onTaskUpdate?: (task: Task) => void;
  onTaskCreated?: (task: Task) => void;
  onTaskDeleted?: (taskId: string) => void;
}

export const useConversationalOrchestrator = ({
  userId,
  onTaskUpdate,
  onTaskCreated,
  onTaskDeleted
}: ConversationalOrchestratorProps) => {
  const [messages, setMessages] = useState<UserMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  // Initialize with a welcome message
  useEffect(() => {
    setMessages([
      {
        id: 'welcome',
        text: 'Hello! I\'m your AI assistant. You can ask me to add, update, or manage your tasks. Try saying "Add a task to buy groceries"',
        sender: 'ai',
        timestamp: new Date()
      }
    ]);
  }, []);

  const processUserMessage = async (input: string) => {
    // Cancel any ongoing request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create new abort controller for this request
    abortControllerRef.current = new AbortController();
    
    // Add user message to the conversation
    const userMessage: UserMessage = {
      id: Date.now().toString(),
      text: input,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Check if the input is in Urdu
      const isUrdu = IntentParserAgent.isUrdu(input);

      // Parse the intent from user input using both rule-based and enhanced classification
      let intentResult = await IntentParserAgent.parseIntent(input);
      
      // Use enhanced classification if available and has higher confidence
      const enhancedIntent = await EnhancedIntentClassifier.classifyIntent(input);
      if (enhancedIntent && enhancedIntent !== 'UNKNOWN') {
        // Map the enhanced intent to our standard intents
        const mappedIntent = mapEnhancedIntent(enhancedIntent);
        if (mappedIntent && intentResult.confidence < 0.8) { // Only override if low confidence in rule-based
          intentResult = {
            ...intentResult,
            intent: mappedIntent
          };
        }
      }

      // Prepare tool request based on parsed intent
      const toolRequest: ToolRequest = {
        action: getIntentAction(intentResult.intent),
        userId,
        params: intentResult.entities
      };

      // Execute the appropriate action based on intent
      const toolResult = await MCPToolExecutorPhaseIII.execute(toolRequest);

      // Format the response
      const formattedResponse = await ReplyFormatter.formatWithLanguage(
        toolResult, 
        intentResult.intent, 
        isUrdu
      );

      // Add AI response to the conversation
      const aiMessage: UserMessage = {
        id: (Date.now() + 1).toString(),
        text: formattedResponse,
        sender: 'ai',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);

      // Trigger appropriate callbacks based on action
      switch (intentResult.intent) {
        case IntentType.CREATE_TASK:
          if (toolResult.task) {
            onTaskCreated?.(toolResult.task);
          }
          break;
        case IntentType.UPDATE_TASK:
          if (toolResult.task) {
            onTaskUpdate?.(toolResult.task);
          }
          break;
        case IntentType.DELETE_TASK:
          if (toolResult.taskId) {
            onTaskDeleted?.(toolResult.taskId);
          }
          break;
        default:
          break;
      }
    } catch (error: any) {
      if (error.name === 'AbortError') {
        // Request was cancelled, don't show error
        return;
      }
      
      console.error('Error processing user message:', error);
      
      const errorMessage: UserMessage = {
        id: (Date.now() + 1).toString(),
        text: 'Sorry, I encountered an error processing your request. Could you please try again?',
        sender: 'ai',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      abortControllerRef.current = null;
    }
  };

  const clearConversation = () => {
    setMessages([
      {
        id: 'welcome',
        text: 'Hello! I\'m your AI assistant. You can ask me to add, update, or manage your tasks. Try saying "Add a task to buy groceries"',
        sender: 'ai',
        timestamp: new Date()
      }
    ]);
  };

  return {
    messages,
    isLoading,
    processUserMessage,
    clearConversation
  };
};

// Helper function to map intent to action
function getIntentAction(intent: IntentType): string {
  switch (intent) {
    case IntentType.CREATE_TASK:
      return 'create_task';
    case IntentType.UPDATE_TASK:
      return 'update_task';
    case IntentType.DELETE_TASK:
      return 'delete_task';
    case IntentType.COMPLETE_TASK:
      return 'complete_task';
    case IntentType.LIST_TASKS:
      return 'list_tasks';
    case IntentType.SEARCH_TASKS:
      return 'search_tasks';
    default:
      return 'unknown';
  }
}

// Helper function to map enhanced intent to standard intent
function mapEnhancedIntent(enhancedIntent: string): IntentType | null {
  switch (enhancedIntent.toUpperCase()) {
    case 'CREATE_TASK':
      return IntentType.CREATE_TASK;
    case 'UPDATE_TASK':
      return IntentType.UPDATE_TASK;
    case 'DELETE_TASK':
      return IntentType.DELETE_TASK;
    case 'COMPLETE_TASK':
      return IntentType.COMPLETE_TASK;
    case 'LIST_TASKS':
      return IntentType.LIST_TASKS;
    case 'SEARCH_TASKS':
      return IntentType.SEARCH_TASKS;
    default:
      return null;
  }
}