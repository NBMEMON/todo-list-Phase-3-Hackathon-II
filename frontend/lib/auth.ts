// Auth utility functions for token handling
import { jwtDecode } from 'jwt-decode'; // You would install this package

// Define types for our tokens and user
interface TokenType {
  user_id: string;
  email: string;
  exp: number;
  iat: number;
}

interface User {
  id: string;
  email: string;
  username?: string;
  name?: string;
}

/**
 * Store authentication tokens in localStorage
 */
export const setTokens = (accessToken: string, refreshToken: string): void => {
  localStorage.setItem('access_token', accessToken);
  localStorage.setItem('refresh_token', refreshToken);
};

/**
 * Get stored tokens from localStorage
 */
export const getTokens = (): { accessToken: string | null; refreshToken: string | null } => {
  if (typeof window === 'undefined') {
    // Server-side, return null
    return { accessToken: null, refreshToken: null };
  }

  const accessToken = localStorage.getItem('access_token');
  const refreshToken = localStorage.getItem('refresh_token');
  return { accessToken, refreshToken };
};

/**
 * Remove tokens from localStorage
 */
export const removeTokens = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }
};

/**
 * Check if access token is expired
 */
export const isAccessTokenExpired = (token: string | null): boolean => {
  if (!token || typeof window === 'undefined') return true;

  try {
    const decoded: TokenType = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  } catch (error) {
    console.error('Error decoding token:', error);
    return true;
  }
};

/**
 * Check if refresh token is expired
 */
export const isRefreshTokenExpired = (token: string | null): boolean => {
  if (!token || typeof window === 'undefined') return true;

  try {
    const decoded: TokenType = jwtDecode(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp < currentTime;
  } catch (error) {
    console.error('Error decoding refresh token:', error);
    return true;
  }
};

/**
 * Get current user from access token
 */
export const getCurrentUser = (): User | null => {
  if (typeof window === 'undefined') return null;

  const { accessToken } = getTokens();
  if (!accessToken || isAccessTokenExpired(accessToken)) {
    return null;
  }

  try {
    const decoded: TokenType = jwtDecode(accessToken);
    return {
      id: decoded.user_id,
      email: decoded.email,
    };
  } catch (error) {
    console.error('Error getting current user:', error);
    return null;
  }
};

let refreshPromise: Promise<string | null> | null = null;

/**
 * Refresh access token using refresh token
 */
export const refreshAccessToken = async (): Promise<string | null> => {
  // Check if we're in the browser
  if (typeof window === 'undefined') {
    return null;
  }

  const { refreshToken } = getTokens();

  if (!refreshToken || isRefreshTokenExpired(refreshToken)) {
    removeTokens();
    return null;
  }

  // If a refresh operation is already in progress, return the existing promise
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = (async () => {
    try {
      // In a real implementation, this would call the backend refresh endpoint
      const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:8000'}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'refresh_token': refreshToken, // Pass refresh token in header
        },
      });

      if (response.ok) {
        const data = await response.json();
        const newAccessToken = data.access_token;
        const oldTokens = getTokens();
        setTokens(newAccessToken, oldTokens.refreshToken!);
        return newAccessToken;
      } else {
        removeTokens();
        return null;
      }
    } catch (error) {
      console.error('Error refreshing access token:', error);
      removeTokens();
      return null;
    } finally {
      refreshPromise = null;
    }
  })();

  return refreshPromise;
};

/**
 * Authenticate user by storing tokens
 */
export const authenticateUser = (accessToken: string, refreshToken: string): void => {
  if (typeof window !== 'undefined') {
    setTokens(accessToken, refreshToken);
  }
};

/**
 * Logout user by removing tokens
 */
export const logoutUser = (): void => {
  if (typeof window !== 'undefined') {
    removeTokens();
  }
};