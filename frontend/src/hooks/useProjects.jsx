import { useState, useEffect } from 'react';

export const useProjects = () => {
  const [projects, setProjects] = useState([]);
  const [currentProject, setCurrentProject] = useState(null);

  useEffect(() => {
    try {
      // Load projects from localStorage
      const savedProjects = localStorage.getItem('ai-pm-projects');
      if (savedProjects) {
        const parsed = JSON.parse(savedProjects);
        setProjects(parsed.map((p) => ({
          ...p,
          createdAt: new Date(p.createdAt),
          updatedAt: new Date(p.updatedAt)
        })));
      }
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  }, []);

  const saveProjects = (updatedProjects) => {
    setProjects(updatedProjects);
    localStorage.setItem('ai-pm-projects', JSON.stringify(updatedProjects));
  };

  const createProject = (name, description) => {
    const newProject = {
      id: `project-${Date.now()}`,
      name,
      description,
      createdAt: new Date(),
      updatedAt: new Date(),
      status: 'draft',
      roadmapNodes: []
    };
    
    const updatedProjects = [...projects, newProject];
    saveProjects(updatedProjects);
    setCurrentProject(newProject);
    return newProject;
  };

  const updateProject = (projectId, updates) => {
    const updatedProjects = projects.map(p => 
      p.id === projectId 
        ? { ...p, ...updates, updatedAt: new Date() }
        : p
    );
    saveProjects(updatedProjects);
    
    if (currentProject?.id === projectId) {
      setCurrentProject(prev => prev ? { ...prev, ...updates, updatedAt: new Date() } : null);
    }
  };

  const deleteProject = (projectId) => {
    const updatedProjects = projects.filter(p => p.id !== projectId);
    saveProjects(updatedProjects);
    
    if (currentProject?.id === projectId) {
      setCurrentProject(null);
    }
  };

  const selectProject = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    setCurrentProject(project || null);
  };

  return {
    projects,
    currentProject,
    createProject,
    updateProject,
    deleteProject,
    selectProject,
    setCurrentProject
  };
};
