'use client';

import { ToolExecutionResult } from '@/lib/ai/mcp-tool-executor';
import { IntentType } from '@/lib/ai/intent-parser';

export class ReplyFormatter {
  /**
   * Formats the tool execution result into a natural language response
   * @param result The result from the tool execution
   * @param intentType The type of intent that triggered the action
   * @returns Formatted response string
   */
  static async format(result: ToolExecutionResult, intentType: IntentType): Promise<string> {
    if (!result.success) {
      return this.formatErrorResponse(result);
    }

    switch (intentType) {
      case IntentType.CREATE_TASK:
        return this.formatCreateTaskResponse(result);
      case IntentType.UPDATE_TASK:
        return this.formatUpdateTaskResponse(result);
      case IntentType.DELETE_TASK:
        return this.formatDeleteTaskResponse(result);
      case IntentType.COMPLETE_TASK:
        return this.formatCompleteTaskResponse(result);
      case IntentType.LIST_TASKS:
        return this.formatListTasksResponse(result);
      case IntentType.SEARCH_TASKS:
        return this.formatSearchTasksResponse(result);
      default:
        return this.formatGenericResponse(result);
    }
  }

  /**
   * Formats response for create task action
   */
  private static formatCreateTaskResponse(result: ToolExecutionResult): string {
    if (result.task) {
      return `✅ Great! I've created the task "${result.task.title}". You can find it in your task list.`;
    }
    return "✅ Task created successfully!";
  }

  /**
   * Formats response for update task action
   */
  private static formatUpdateTaskResponse(result: ToolExecutionResult): string {
    if (result.task) {
      return `✏️ Task "${result.task.title}" has been updated successfully.`;
    }
    return "✏️ Task updated successfully!";
  }

  /**
   * Formats response for delete task action
   */
  private static formatDeleteTaskResponse(result: ToolExecutionResult): string {
    if (result.taskId) {
      return "🗑️ Task has been deleted successfully.";
    }
    return "🗑️ Task deleted successfully!";
  }

  /**
   * Formats response for complete task action
   */
  private static formatCompleteTaskResponse(result: ToolExecutionResult): string {
    if (result.task) {
      const status = result.task.completed ? "completed" : "marked as incomplete";
      return `✔️ Task "${result.task.title}" has been ${status}.`;
    }
    return "✔️ Task status updated!";
  }

  /**
   * Formats response for list tasks action
   */
  private static formatListTasksResponse(result: ToolExecutionResult): string {
    if (result.tasks && result.tasks.length > 0) {
      const total = result.tasks.length;
      const completed = result.tasks.filter(t => t.completed).length;
      const pending = total - completed;
      
      if (total === 1) {
        const task = result.tasks[0];
        const status = task.completed ? "✅" : "⏳";
        return `📋 You have 1 task: ${status} ${task.title}`;
      }
      
      return `📋 You have ${total} tasks in total: ${pending} pending and ${completed} completed.`;
    }
    
    return "📋 You don't have any tasks yet. Would you like to add one?";
  }

  /**
   * Formats response for search tasks action
   */
  private static formatSearchTasksResponse(result: ToolExecutionResult): string {
    if (result.tasks && result.tasks.length > 0) {
      const count = result.tasks.length;
      if (count === 1) {
        return `🔍 Found 1 task matching your search.`;
      }
      return `🔍 Found ${count} tasks matching your search.`;
    }
    
    return result.message || "🔍 No tasks found matching your search.";
  }

  /**
   * Formats generic response for unknown intent
   */
  private static formatGenericResponse(result: ToolExecutionResult): string {
    return result.message || "Action completed successfully.";
  }

  /**
   * Formats error response
   */
  private static formatErrorResponse(result: ToolExecutionResult): string {
    const errorMessage = result.error || result.message || "An error occurred while processing your request.";
    
    // Common error responses
    if (errorMessage.includes('Authentication required')) {
      return "🔒 It looks like you need to log in first. Please log in to continue using the service.";
    }
    
    if (errorMessage.includes('Task ID is required')) {
      return "🤔 I need to know which task you're referring to. Could you please specify the task?";
    }
    
    if (errorMessage.includes('Title is required')) {
      return "📝 Please provide a title for the task you'd like to create.";
    }
    
    return `❌ ${errorMessage} Could you please try rephrasing your request?`;
  }

  /**
   * Detects if the user's original input was in Urdu
   * @param userInput The original user input
   * @returns True if the input is in Urdu, false otherwise
   */
  static detectUrdu(userInput: string): boolean {
    // Urdu uses Arabic script, so we check for Arabic/Urdu characters
    const urduRegex = /[\u0600-\u06FF\u0750-\u077F]/;
    return urduRegex.test(userInput);
  }

  /**
   * Generates a response in Urdu if the input was in Urdu
   * @param result The result from the tool execution
   * @param intentType The type of intent that triggered the action
   * @param isUrdu Whether the input was in Urdu
   * @returns Formatted response string in appropriate language
   */
  static async formatWithLanguage(result: ToolExecutionResult, intentType: IntentType, isUrdu: boolean): Promise<string> {
    if (isUrdu) {
      // For now, return English responses with Urdu script note
      // In a full implementation, we would have Urdu translations
      const englishResponse = await this.format(result, intentType);
      return `${englishResponse} (Note: Urdu language support coming soon!)`;
    }
    
    return await this.format(result, intentType);
  }
}