import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import ApiClient from '../services/api';

export const useProjects = () => {
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user, isAuthenticated } = useAuth();

  // Load projects from API when user is authenticated
  useEffect(() => {
    if (isAuthenticated && user) {
      loadProjects();
    } else {
      // Clear projects when not authenticated
      setProjects([]);
      setCurrentProject(null);
      setError(null);
    }
  }, [isAuthenticated, user]);

  const loadProjects = async () => {
    // Check if user is authenticated
    if (!isAuthenticated || !user) {
      console.log('User not authenticated, skipping project load');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const projectsData = await ApiClient.getUserProjects();
      
      // Convert API response to frontend format
      const formattedProjects = projectsData.map(project => ({
        id: project.id,
        name: project.name,
        description: project.description,
        status: project.status,
        createdAt: new Date(project.created_at),
        updatedAt: new Date(project.updated_at),
        roadmapNodes: project.roadmap_data?.nodes || []
      }));
      
      setProjects(formattedProjects);
    } catch (error) {
      console.error('Failed to load projects:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const createProject = async (name, description) => {
    // Check if user is authenticated
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to create projects');
    }

    try {
      setLoading(true);
      setError(null);
      
      // Create project via API
      const newProject = await ApiClient.createProject(name, description);
      
      // Format for frontend
      const formattedProject = {
        id: newProject.id,
        name: newProject.name,
        description: newProject.description,
        status: newProject.status,
        createdAt: new Date(newProject.created_at),
        updatedAt: new Date(newProject.updated_at),
        roadmapNodes: []
      };
      
      // Add to local state
      setProjects(prev => [formattedProject, ...prev]);
      setCurrentProject(formattedProject);
      
      return formattedProject;
    } catch (error) {
      console.error('Failed to create project:', error);
      setError(error.message);
      throw error; // Re-throw to let caller handle the error
    } finally {
      setLoading(false);
    }
  };

  const updateProject = async (projectId, updates) => {
    // Check if user is authenticated
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to update projects');
    }

    try {
      setLoading(true);
      setError(null);
      
      // Update via API
      const updatedProject = await ApiClient.updateProject(projectId, updates);
      
      // Format for frontend
      const formattedProject = {
        id: updatedProject.id,
        name: updatedProject.name,
        description: updatedProject.description,
        status: updatedProject.status,
        createdAt: new Date(updatedProject.created_at),
        updatedAt: new Date(updatedProject.updated_at),
        roadmapNodes: updatedProject.roadmap_data?.nodes || []
      };
      
      // Update local state
      setProjects(prev => 
        prev.map(p => p.id === projectId ? formattedProject : p)
      );
      
      if (currentProject?.id === projectId) {
        setCurrentProject(formattedProject);
      }
      
      return formattedProject;
    } catch (error) {
      console.error('Failed to update project:', error);
      setError(error.message);
      throw error; // Re-throw to let caller handle the error
    } finally {
      setLoading(false);
    }
  };

  const deleteProject = async (projectId) => {
    // Check if user is authenticated
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to delete projects');
    }

    try {
      setLoading(true);
      setError(null);
      
      // Delete via API
      await ApiClient.deleteProject(projectId);
      
      // Remove from local state
      setProjects(prev => prev.filter(p => p.id !== projectId));
      
      if (currentProject?.id === projectId) {
        setCurrentProject(null);
      }
    } catch (error) {
      console.error('Failed to delete project:', error);
      setError(error.message);
      throw error; // Re-throw to let caller handle the error
    } finally {
      setLoading(false);
    }
  };

  const selectProject = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    setCurrentProject(project || null);
  };

  const refreshProjects = () => {
    loadProjects();
  };

  return {
    projects,
    currentProject,
    loading,
    error,
    createProject,
    updateProject,
    deleteProject,
    selectProject,
    setCurrentProject,
    refreshProjects
  };
};
