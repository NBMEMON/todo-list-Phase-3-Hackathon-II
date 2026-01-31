import { getTokens, refreshAccessToken, isAccessTokenExpired } from './auth';

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

/**
 * Generic API request function with JWT token handling
 */
export const apiRequest = async <T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> => {
  let { accessToken } = getTokens();

  // Check if access token is expired and refresh if needed
  if (accessToken && isAccessTokenExpired(accessToken)) {
    accessToken = await refreshAccessToken();
  }

  const headers = {
    'Content-Type': 'application/json',
    ...(accessToken && { Authorization: `Bearer ${accessToken}` }),
    ...options.headers,
  };

  try {
    const response = await fetch(`${BASE_URL}${endpoint}`, {
      ...options,
      headers,
    });

    if (response.status === 401) {
      // Token might be invalid, try to refresh and retry
      const newAccessToken = await refreshAccessToken();
      if (newAccessToken) {
        const retryResponse = await fetch(`${BASE_URL}${endpoint}`, {
          ...options,
          headers: {
            ...headers,
            Authorization: `Bearer ${newAccessToken}`,
          },
        });

        if (!retryResponse.ok) {
          throw new Error(`HTTP error! status: ${retryResponse.status}`);
        }

        return { data: await retryResponse.json() };
      } else {
        // If refresh failed, redirect to login
        window.location.href = '/login';
        return { error: 'Authentication required' };
      }
    }

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return { data: await response.json() };
  } catch (error) {
    console.error('API request error:', error);
    return { error: (error as Error).message };
  }
};

/**
 * Specific API functions for user operations
 */
export const userApi = {
  // Get current user profile
  getCurrentUser: async () => {
    return apiRequest<User>('/api/v1/users/me');
  },
};

/**
 * Specific API functions for task operations
 */
export const taskApi = {
  // Get user's tasks
  getUserTasks: async (userId: string) => {
    return apiRequest<Task[]>(`/api/v1/${userId}/tasks`);
  },

  // Create a new task
  createTask: async (userId: string, taskData: { title: string; description?: string; priority?: number }) => {
    return apiRequest(`/api/v1/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  },

  // Get specific task
  getTask: async (userId: string, taskId: string) => {
    return apiRequest<Task>(`/api/v1/${userId}/tasks/${taskId}`);
  },

  // Update task
  updateTask: async (userId: string, taskId: string, taskData: Partial<Task>) => {
    return apiRequest(`/api/v1/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  },

  // Toggle task completion
  toggleTaskCompletion: async (userId: string, taskId: string, completed: boolean) => {
    return apiRequest(`/api/v1/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
      body: JSON.stringify({ completed }),
    });
  },

  // Delete task
  deleteTask: async (userId: string, taskId: string) => {
    return apiRequest(`/api/v1/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    });
  },
};

// Define TypeScript interfaces
export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: number;  // Priority levels 1-5, with 1 being highest
  user_id: string;
  created_at: string;
  updated_at: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}