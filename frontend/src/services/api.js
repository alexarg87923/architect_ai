const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
const API_TIMEOUT = import.meta.env.VITE_API_TIMEOUT || 30000;

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.timeout = API_TIMEOUT;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      timeout: this.timeout,
      ...options,
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        // Try to get the error detail from the response
        let errorDetail = response.statusText;
        try {
          const errorData = await response.json();
          if (errorData.detail) {
            errorDetail = errorData.detail;
          }
        } catch (e) {
          // If we can't parse the error response, use the status text
        }
        throw new Error(`HTTP ${response.status}: ${errorDetail}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error(`API request failed: ${error.message}`);
      throw error;
    }
  }

  // Agent API Methods
  async chatWithAgent(message, sessionId = null, actionType = 'chat', conversationState = null) {
    const userId = localStorage.getItem('user_id');
    
    const response = await this.request('/api/agent/chat', {
      method: 'POST',
      body: {
        message,
        session_id: sessionId,
        action_type: actionType,
        conversation_state: conversationState,
        user_id: userId ? parseInt(userId) : null
      },
    });
    
    // Return structured response with session management
    return {
      agentResponse: response.agent_response,
      conversationState: response.conversation_state,
      sessionId: response.session_id,
      actionButton: response.action_button,
      currentRoadmap: response.conversation_state?.current_roadmap,
      phase: response.conversation_state?.phase,
    };
  }

  // Simulation API Methods
  async getProjectOptions() {
    const response = await this.request('/api/simulation/project-options', {
      method: 'GET',
    });
    
    return {
      success: response.success,
      projectOptions: response.project_options
    };
  }

  async runSimulation(projectId, projectType = 'codementor') {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await this.request(`/api/simulation/run?user_id=${parseInt(userId)}&project_id=${projectId}&project_type=${projectType}`, {
      method: 'POST',
    });
    
    return {
      success: response.success,
      sessionId: response.session_id,
      conversationState: response.conversation_state,
      messages: response.messages,
      roadmap: response.roadmap,
      totalRounds: response.total_rounds
    };
  }

  async getConversation(sessionId) {
    const response = await this.request(`/api/agent/conversation/${sessionId}`);
    return {
      conversationState: response,
      messages: response.messages || [],
      phase: response.phase,
      specificationsComplete: response.specifications_complete,
    };
  }

  async getRoadmap(sessionId) {
    const response = await this.request(`/api/agent/roadmap/${sessionId}`);
    return {
      roadmap: response.roadmap,
      message: response.message,
      projectTitle: response.roadmap?.project_specification?.title,
      nodes: response.roadmap?.nodes || [],
      totalWeeks: response.roadmap?.total_estimated_weeks,
      totalHours: response.roadmap?.total_estimated_hours,
    };
  }

  async deleteConversation(sessionId) {
    return this.request(`/api/agent/conversation/${sessionId}`, {
      method: 'DELETE',
    });
  }

  async getAgentHealth() {
    return this.request('/api/agent/health');
  }

  // Roadmap API Methods
  async getRoadmapHealth() {
    return this.request('/api/roadmap/health');
  }

  // Chat API Methods  
  async getChatHealth() {
    return this.request('/api/chat/health');
  }

  // General API Methods
  async getHealth() {
    return this.request('/health');
  }

  // Project API Methods
  async createProject(name, description, status = 'draft') {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects?user_id=${userId}`, {
      method: 'POST',
      body: {
        name,
        description,
        status
      }
    });
  }

  async getUserProjects() {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects?user_id=${userId}`);
  }

  async getProject(projectId) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}?user_id=${userId}`);
  }

  async updateProject(projectId, updates) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}?user_id=${userId}`, {
      method: 'PUT',
      body: updates
    });
  }

  async deleteProject(projectId) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}?user_id=${userId}`, {
      method: 'DELETE'
    });
  }

  async updateProjectRoadmap(projectId, roadmap) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}/roadmap?user_id=${userId}`, {
      method: 'PUT',
      body: roadmap
    });
  }

  // Task API Methods
  async createTask(projectId, text, taskType) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}/tasks?user_id=${userId}`, {
      method: 'POST',
      body: {
        text,
        task_type: taskType,
        completed: false
      }
    });
  }

  async updateTask(projectId, taskId, updates) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}/tasks/${taskId}?user_id=${userId}`, {
      method: 'PUT',
      body: updates
    });
  }

  async deleteTask(projectId, taskId) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    return this.request(`/api/projects/${projectId}/tasks/${taskId}?user_id=${userId}`, {
      method: 'DELETE'
    });
  }

  async getProjectTasks(projectId) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await this.request(`/api/projects/${projectId}/tasks?user_id=${parseInt(userId)}`, {
      method: 'GET',
    });
    
    return response;
  }

  // Auth API Methods
  async changePassword(currentPassword, newPassword, confirmPassword) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await this.request(`/api/auth/change-password?user_id=${parseInt(userId)}`, {
      method: 'POST',
      body: {
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword
      },
    });
    
    return response;
  }

  // Feedback API Methods
  async submitFeedback(feedbackType, message) {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await this.request(`/api/feedback/submit?user_id=${parseInt(userId)}`, {
      method: 'POST',
      body: {
        feedback_type: feedbackType,
        message: message
      },
    });
    
    return response;
  }

  async getUserFeedback() {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      throw new Error('User not authenticated');
    }

    const response = await this.request(`/api/feedback/user?user_id=${parseInt(userId)}`, {
      method: 'GET',
    });
    
    return response;
  }

  async getAllFeedback() {
    const response = await this.request('/api/admin/feedback', {
      method: 'GET',
    });
    
    return response;
  }

  async updateFeedback(feedbackId, status, adminNotes) {
    const response = await this.request(`/api/admin/feedback/${feedbackId}`, {
      method: 'PATCH',
      body: {
        status: status,
        admin_notes: adminNotes
      },
    });
    
    return response;
  }

  async deleteFeedback(feedbackId) {
    const response = await this.request(`/api/admin/feedback/${feedbackId}`, {
      method: 'DELETE',
    });
    
    return response;
  }

  // Utility methods for roadmap data processing
  formatRoadmapForDisplay(roadmap) {
    if (!roadmap) return null;
    
    return {
      title: roadmap.project_specification?.title || 'Untitled Project',
      description: roadmap.project_specification?.description || '',
      totalWeeks: roadmap.total_estimated_weeks || 0,
      totalHours: roadmap.total_estimated_hours || 0,
      nodes: roadmap.nodes?.map(node => ({
        id: node.id,
        title: node.title,
        description: node.description,
        estimatedDays: node.estimated_days,
        estimatedHours: node.estimated_hours,
        tags: node.tags || [],
        dependencies: node.dependencies || [],
        status: node.status || 'pending',
        completionPercentage: node.completion_percentage || 0,
        deliverables: node.deliverables || [],
        successCriteria: node.success_criteria || [],
        subtasks: node.subtasks?.map(subtask => ({
          id: subtask.id,
          title: subtask.title,
          description: subtask.description,
          completed: subtask.completed || false,
          estimatedHours: subtask.estimated_hours || 0,
        })) || [],
      })) || [],
    };
  }

  // Check if agent is ready for specific actions
  isReadyForRoadmapGeneration(conversationState) {
    return conversationState?.phase === 'confirmation' || 
           conversationState?.specifications_complete === true;
  }

  isInEditingPhase(conversationState) {
    return conversationState?.phase === 'editing' && 
           conversationState?.current_roadmap !== null;
  }

  hasRoadmap(conversationState) {
    return conversationState?.current_roadmap !== null;
  }
}

export default new ApiClient();
