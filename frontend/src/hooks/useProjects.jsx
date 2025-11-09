import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useSelectedProject } from '../contexts/SelectedProjectContext';
import ApiClient from '../services/api';

export const useProjects = () => {
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user, isAuthenticated } = useAuth();
  const { selectedProject, updateSelectedProject } = useSelectedProject();

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
        roadmapNodes: project.roadmap_data?.nodes || [],
        tasks: project.tasks ? {
          "daily-todos": project.tasks.daily_todos.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          })),
          "your-ideas": project.tasks.your_ideas.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          }))
        } : {
          "daily-todos": [],
          "your-ideas": []
        }
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
      
      // Format for frontend with default tasks
      const formattedProject = {
        id: newProject.id,
        name: newProject.name,
        description: newProject.description,
        status: newProject.status,
        createdAt: new Date(newProject.created_at),
        updatedAt: new Date(newProject.updated_at),
        roadmapNodes: [],
        tasks: newProject.tasks ? {
          "daily-todos": newProject.tasks.daily_todos.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          })),
          "your-ideas": newProject.tasks.your_ideas.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          }))
        } : {
          "daily-todos": [],
          "your-ideas": []
        }
      };
      
      // Add to local state
      setProjects(prev => [...prev, formattedProject]);
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
        roadmapNodes: updatedProject.roadmap_data?.nodes || [],
        tasks: updatedProject.tasks ? {
          "daily-todos": updatedProject.tasks.daily_todos.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          })),
          "your-ideas": updatedProject.tasks.your_ideas.map(task => ({
            id: task.id,
            text: task.text,
            completed: task.completed,
            archive: task.archive || false
          }))
        } : {
          "daily-todos": [],
          "your-ideas": []
        }
      };
      
      // Update local state
      setProjects(prev => 
        prev.map(p => p.id === projectId ? formattedProject : p)
      );
      
      if (currentProject?.id === projectId) {
        setCurrentProject(formattedProject);
      }
      
      // Update selected project in context if it's the same project
      if (selectedProject?.id === projectId) {
        updateSelectedProject(formattedProject);
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

  // Task operations
  const createTask = async (projectId, text, taskType) => {
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to create tasks');
    }

    try {
      setLoading(true);
      setError(null);
      
      const newTask = await ApiClient.createTask(projectId, text, taskType);
      
      // Update local state
      setProjects(prev => 
        prev.map(project => {
          if (project.id === projectId) {
            return {
              ...project,
              tasks: {
                ...project.tasks,
                [taskType]: [...project.tasks[taskType], {
                  id: newTask.id,
                  text: newTask.text,
                  completed: newTask.completed,
                  archive: newTask.archive || false

                }]
              }
            };
          }
          return project;
        })
      );
      
      // Update current project if it's the one being modified
      if (currentProject?.id === projectId) {
        const updatedCurrentProject = {
          ...currentProject,
          tasks: {
            ...currentProject.tasks,
            [taskType]: [...currentProject.tasks[taskType], {
              id: newTask.id,
              text: newTask.text,
              completed: newTask.completed,
              archive: newTask.archive || false
            }]
          }
        };
        setCurrentProject(updatedCurrentProject);
      }
      
      // Update selected project in context if it's the same project
      if (selectedProject?.id === projectId) {
        const updatedSelectedProject = {
          ...selectedProject,
          tasks: {
            ...selectedProject.tasks,
            [taskType]: [...selectedProject.tasks[taskType], {
              id: newTask.id,
              text: newTask.text,
              completed: newTask.completed,
              archive: newTask.archive || false

            }]
          }
        };
        updateSelectedProject(updatedSelectedProject);
      }
      
      return newTask;
    } catch (error) {
      console.error('Failed to create task:', error);
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (projectId, taskId, updates) => {
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to update tasks');
    }

    try {
      setLoading(true);
      setError(null);
      
      const updatedTask = await ApiClient.updateTask(projectId, taskId, updates);
      
      // Update local state
      setProjects(prev => 
        prev.map(project => {
          if (project.id === projectId) {
            return {
              ...project,
              tasks: {
                "daily-todos": project.tasks["daily-todos"].map(task => 
                  task.id === taskId ? { ...task, ...updates } : task
                ),
                "your-ideas": project.tasks["your-ideas"].map(task => 
                  task.id === taskId ? { ...task, ...updates } : task
                )
              }
            };
          }
          return project;
        })
      );
      
      // Update current project if it's the one being modified
      if (currentProject?.id === projectId) {
        const updatedCurrentProject = {
          ...currentProject,
          tasks: {
            "daily-todos": currentProject.tasks["daily-todos"].map(task => 
              task.id === taskId ? { ...task, ...updates } : task
            ),
            "your-ideas": currentProject.tasks["your-ideas"].map(task => 
              task.id === taskId ? { ...task, ...updates } : task
            )
          }
        };
        setCurrentProject(updatedCurrentProject);
      }
      
      // Update selected project in context if it's the same project
      if (selectedProject?.id === projectId) {
        const updatedSelectedProject = {
          ...selectedProject,
          tasks: {
            "daily-todos": selectedProject.tasks["daily-todos"].map(task => 
              task.id === taskId ? { ...task, ...updates } : task
            ),
            "your-ideas": selectedProject.tasks["your-ideas"].map(task => 
              task.id === taskId ? { ...task, ...updates } : task
            )
          }
        };
        updateSelectedProject(updatedSelectedProject);
      }
      
      return updatedTask;
    } catch (error) {
      console.error('Failed to update task:', error);
      setError(error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const deleteTask = async (projectId, taskId, taskType) => {
    if (!isAuthenticated || !user) {
      throw new Error('User must be authenticated to delete tasks');
    }

    try {
      setLoading(true);
      setError(null);
      
      await ApiClient.deleteTask(projectId, taskId);
      
      // Update local state
      setProjects(prev => 
        prev.map(project => {
          if (project.id === projectId) {
            return {
              ...project,
              tasks: {
                ...project.tasks,
                [taskType]: project.tasks[taskType].filter(task => task.id !== taskId)
              }
            };
          }
          return project;
        })
      );
      
      // Update current project if it's the one being modified
      if (currentProject?.id === projectId) {
        const updatedCurrentProject = {
          ...currentProject,
          tasks: {
            ...currentProject.tasks,
            [taskType]: currentProject.tasks[taskType].filter(task => task.id !== taskId)
          }
        };
        setCurrentProject(updatedCurrentProject);
      }
      
      // Update selected project in context if it's the same project
      if (selectedProject?.id === projectId) {
        const updatedSelectedProject = {
          ...selectedProject,
          tasks: {
            ...selectedProject.tasks,
            [taskType]: selectedProject.tasks[taskType].filter(task => task.id !== taskId)
          }
        };
        updateSelectedProject(updatedSelectedProject);
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
      setError(error.message);
      throw error;
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
    createTask,
    updateTask,
    deleteTask,
    selectProject,
    setCurrentProject,
    refreshProjects
  };
};
