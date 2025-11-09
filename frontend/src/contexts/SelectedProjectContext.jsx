import React, { createContext, useContext, useState, useEffect } from 'react';

const ProjectContext = createContext();

const SELECTED_PROJECT_KEY = 'roadmap-selected-project';

export const ProjectProvider = ({ children }) => {
  // Initialize selectedProject from localStorage if available
  const [selectedProject, setSelectedProject] = useState(() => {
    try {
      const saved = localStorage.getItem(SELECTED_PROJECT_KEY);
      return saved ? JSON.parse(saved) : null;
    } catch (error) {
      console.error('Error loading selected project from localStorage:', error);
      return null;
    }
  });

  // Save to localStorage whenever selectedProject changes
  useEffect(() => {
    try {
      if (selectedProject) {
        localStorage.setItem(SELECTED_PROJECT_KEY, JSON.stringify(selectedProject));
      } else {
        localStorage.removeItem(SELECTED_PROJECT_KEY);
      }
    } catch (error) {
      console.error('Error saving selected project to localStorage:', error);
    }
  }, [selectedProject]);

  const selectProject = (project) => {
    setSelectedProject(project);
  };

  const clearSelection = () => {
    setSelectedProject(null);
  };

  const updateSelectedProject = (updatedProject) => {
    setSelectedProject(updatedProject);
  };

  const updateRoadmapNodes = (updatedNodes) => {
    if (selectedProject) {
      setSelectedProject({
        ...selectedProject,
        roadmapNodes: updatedNodes
      });
    }
  };

  return (
    <ProjectContext.Provider value={{
      selectedProject,
      selectProject,
      clearSelection,
      updateSelectedProject,
      updateRoadmapNodes
    }}>
      {children}
    </ProjectContext.Provider>
  );
};

export const useSelectedProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error('useSelectedProject must be used within a ProjectProvider');
  }
  return context;
};
