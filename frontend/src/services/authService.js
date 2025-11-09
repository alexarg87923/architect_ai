// AuthService for Roadmap AI
// Handles authentication API calls to the backend

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

class AuthService {
  /**
   * Login user with email (dev mode - no password required)
   */
  async login(email, password = null) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Login failed');
      }

      const data = await response.json();
      
      // Store auth data in localStorage
      localStorage.setItem('auth_token', `dev-token-${data.user.id}`);
      localStorage.setItem('user', JSON.stringify(data.user));
      localStorage.setItem('user_id', data.user.id.toString());

      return {
        user: data.user,
        token: `dev-token-${data.user.id}`,
        message: data.message
      };
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  /**
   * Get current user from backend
   */
  async getCurrentUser(userId) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/me/${userId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to get user data');
      }

      return await response.json();
    } catch (error) {
      console.error('Get user error:', error);
      throw error;
    }
  }

  /**
   * Logout user (dev mode - just clear localStorage)
   */
  async logout() {
    try {
      // In production, you would call a logout endpoint
      // For dev, just clear local storage
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      localStorage.removeItem('user_id');
      
      return { message: 'Logged out successfully' };
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    }
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('user');
    return !!(token && user);
  }

  /**
   * Get stored user data
   */
  getStoredUser() {
    try {
      const userData = localStorage.getItem('user');
      return userData ? JSON.parse(userData) : null;
    } catch (error) {
      console.error('Error getting stored user:', error);
      return null;
    }
  }

  /**
   * Get stored user ID
   */
  getStoredUserId() {
    return localStorage.getItem('user_id');
  }
}

export default new AuthService();
