'use client';

import { Task, taskApi } from '@/lib/api';
import { getTokens } from '@/lib/auth';

// Result types for tool execution
export interface ToolExecutionResult {
  success: boolean;
  message: string;
  task?: Task;
  taskId?: string;
  tasks?: Task[];
  error?: string;
}

// Tool request parameters
export interface ToolRequest {
  action: string;
  userId: string;
  params: Record<string, any>;
}

export class MCPToolExecutorPhaseIII {
  /**
   * Executes a tool request based on the parsed intent
   * @param request The tool request with action and parameters
   * @returns Execution result
   */
  static async execute(request: ToolRequest): Promise<ToolExecutionResult> {
    // Validate JWT token before executing any action
    const { accessToken } = getTokens();
    if (!accessToken) {
      return {
        success: false,
        message: 'Authentication required',
        error: 'No access token available'
      };
    }

    try {
      // Route to appropriate handler based on action
      switch (request.action) {
        case 'create_task':
          return await this.handleCreateTask(request.userId, request.params);
        case 'update_task':
          return await this.handleUpdateTask(request.userId, request.params);
        case 'delete_task':
          return await this.handleDeleteTask(request.userId, request.params);
        case 'complete_task':
          return await this.handleCompleteTask(request.userId, request.params);
        case 'list_tasks':
          return await this.handleListTasks(request.userId);
        case 'search_tasks':
          return await this.handleSearchTasks(request.userId, request.params);
        default:
          return {
            success: false,
            message: 'Unknown action requested',
            error: `Action '${request.action}' is not supported`
          };
      }
    } catch (error) {
      console.error('Error executing tool:', error);
      return {
        success: false,
        message: 'An error occurred while executing the requested action',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles creating a new task
   */
  private static async handleCreateTask(userId: string, params: Record<string, any>): Promise<ToolExecutionResult> {
    const { title, description, priority = 3 } = params;

    if (!title) {
      return {
        success: false,
        message: 'Title is required to create a task',
        error: 'Missing title parameter'
      };
    }

    try {
      const response = await taskApi.createTask(userId, {
        title,
        description: description || '',
        priority: priority
      });

      if (response.error) {
        return {
          success: false,
          message: 'Failed to create task',
          error: response.error
        };
      }

      return {
        success: true,
        message: `Task "${title}" has been created successfully`,
        task: response.data as Task
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to create task',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles updating an existing task
   */
  private static async handleUpdateTask(userId: string, params: Record<string, any>): Promise<ToolExecutionResult> {
    const { taskId, title, description, priority, completed } = params;

    if (!taskId) {
      return {
        success: false,
        message: 'Task ID is required to update a task',
        error: 'Missing taskId parameter'
      };
    }

    const updateData: Partial<Task> = {};
    if (title !== undefined) updateData.title = title;
    if (description !== undefined) updateData.description = description;
    if (priority !== undefined) updateData.priority = priority;
    if (completed !== undefined) updateData.completed = completed;

    try {
      const response = await taskApi.updateTask(userId, taskId, updateData);

      if (response.error) {
        return {
          success: false,
          message: 'Failed to update task',
          error: response.error
        };
      }

      return {
        success: true,
        message: `Task has been updated successfully`,
        task: response.data as Task
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to update task',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles deleting a task
   */
  private static async handleDeleteTask(userId: string, params: Record<string, any>): Promise<ToolExecutionResult> {
    const { taskId } = params;

    if (!taskId) {
      return {
        success: false,
        message: 'Task ID is required to delete a task',
        error: 'Missing taskId parameter'
      };
    }

    try {
      const response = await taskApi.deleteTask(userId, taskId);

      if (response.error) {
        return {
          success: false,
          message: 'Failed to delete task',
          error: response.error
        };
      }

      return {
        success: true,
        message: `Task has been deleted successfully`,
        taskId
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to delete task',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles marking a task as complete/incomplete
   */
  private static async handleCompleteTask(userId: string, params: Record<string, any>): Promise<ToolExecutionResult> {
    const { taskId, completed = true } = params;

    if (!taskId) {
      return {
        success: false,
        message: 'Task ID is required to update completion status',
        error: 'Missing taskId parameter'
      };
    }

    try {
      const response = await taskApi.toggleTaskCompletion(userId, taskId, completed);

      if (response.error) {
        return {
          success: false,
          message: 'Failed to update task completion status',
          error: response.error
        };
      }

      return {
        success: true,
        message: `Task has been marked as ${completed ? 'complete' : 'incomplete'}`,
        task: response.data as Task
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to update task completion status',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles listing all tasks for a user
   */
  private static async handleListTasks(userId: string): Promise<ToolExecutionResult> {
    try {
      const response = await taskApi.getUserTasks(userId);

      if (response.error) {
        return {
          success: false,
          message: 'Failed to retrieve tasks',
          error: response.error
        };
      }

      const tasks = response.data as Task[] || [];
      const count = tasks.length;
      const completedCount = tasks.filter(task => task.completed).length;
      const pendingCount = count - completedCount;

      return {
        success: true,
        message: `You have ${count} tasks: ${pendingCount} pending and ${completedCount} completed`,
        tasks,
        task: tasks[0] // Include first task for potential follow-up
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to retrieve tasks',
        error: (error as Error).message
      };
    }
  }

  /**
   * Handles searching for tasks
   */
  private static async handleSearchTasks(userId: string, params: Record<string, any>): Promise<ToolExecutionResult> {
    const { query } = params;

    if (!query) {
      return {
        success: false,
        message: 'Search query is required',
        error: 'Missing query parameter'
      };
    }

    try {
      const response = await taskApi.getUserTasks(userId);

      if (response.error) {
        return {
          success: false,
          message: 'Failed to search tasks',
          error: response.error
        };
      }

      const allTasks = response.data as Task[] || [];
      const filteredTasks = allTasks.filter(task => 
        task.title.toLowerCase().includes(query.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(query.toLowerCase()))
      );

      if (filteredTasks.length === 0) {
        return {
          success: true,
          message: `No tasks found matching "${query}"`
        };
      }

      return {
        success: true,
        message: `Found ${filteredTasks.length} task(s) matching "${query}"`,
        tasks: filteredTasks
      };
    } catch (error) {
      return {
        success: false,
        message: 'Failed to search tasks',
        error: (error as Error).message
      };
    }
  }
}