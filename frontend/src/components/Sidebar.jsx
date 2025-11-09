import React, { useState, useEffect } from 'react';
import { FiPlus, FiFolder, FiUser } from 'react-icons/fi';
import { HiOutlineMap, HiOutlineMoon, HiDotsHorizontal } from 'react-icons/hi';
import NewProjectModal from './NewProjectModal';
import ProjectMenuModal from './ProjectMenuModal';
import { LuPanelLeftClose, LuPanelLeftOpen } from "react-icons/lu";

// *** Need to save the theme_state to localStorage

const Sidebar = ({ className }) => {
  // Mock data and hooks - you'll need to implement these
  const [projects, setProjects] = useState([
    { id: 1, name: 'Sample Project'}, { id: 2, name: 'Sample Project 2'}
  ]);
  const [currentProject, setCurrentProject] = useState(null);
  const [isNewProjectOpen, setIsNewProjectOpen] = useState(false);
  const [isCollapsed, setIsCollapsed] = useState(() => {
    // Load sidebar state from localStorage
    try {
      const savedState = localStorage.getItem('ai-pm-sidebar-collapsed');
      return savedState ? JSON.parse(savedState) : false;
    } catch (error) {
      console.error('Failed to load sidebar state:', error);
      return false;
    }
  });
  const [contextMenu, setContextMenu] = useState({ show: false, x: 0, y: 0, project: null });
  const [editingProject, setEditingProject] = useState(null);
  const [editingName, setEditingName] = useState('');
  const [originalName, setOriginalName] = useState('');

  // Save sidebar state to localStorage whenever it changes
  useEffect(() => {
    try {
      localStorage.setItem('ai-pm-sidebar-collapsed', JSON.stringify(isCollapsed));
    } catch (error) {
      console.error('Failed to save sidebar state:', error);
    }
  }, [isCollapsed]);

  const createProject = (name, description) => {
    const newProject = {
      id: Date.now(),
      name,
      description,
      status: 'draft',
      updatedAt: new Date()
    };
    setProjects([...projects, newProject]);
  };

  const selectProject = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    setCurrentProject(project);
  };

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  const handleRightClick = (e, project) => {
    e.preventDefault();
    setContextMenu({
      show: true,
      x: e.clientX,
      y: e.clientY,
      project
    });
  };

  const closeContextMenu = () => {
    setContextMenu({ show: false, x: 0, y: 0, project: null });
  };

  const handleRename = (projectId, newName) => {
    setProjects(projects.map(p => 
      p.id === projectId 
        ? { ...p, name: newName }
        : p
    ));
  };

  const startRename = (project) => {
    setCurrentProject(project); // Select the project being renamed
    setEditingProject(project.id);
    setEditingName(project.name);
    setOriginalName(project.name); // Store original name for reverting
    closeContextMenu();
  };

  const saveRename = () => {
    if (editingName.trim()) {
      handleRename(editingProject, editingName.trim());
    }
    setEditingProject(null);
    setEditingName('');
    setOriginalName('');
  };

  const cancelRename = () => {
    setEditingProject(null);
    setEditingName('');
    setOriginalName('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      saveRename();
    } else if (e.key === 'Escape') {
      cancelRename();
    }
  };

  const handleDelete = (projectId) => {
    setProjects(projects.filter(p => p.id !== projectId));
    if (currentProject?.id === projectId) {
      setCurrentProject(null);
    }
  };

  return (
    <>
      {/* Collapsed Floating Header */}
      {isCollapsed && (
        <div className="fixed top-0 left-0 z-50 w-70">
          <div className="p-6">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center">
                <HiOutlineMap className="w-5 h-5 text-white" />
              </div>
              <h1 className="font-semibold text-gray-900 flex-1">Roadmap AI</h1>
              <LuPanelLeftOpen 
                className="w-6 h-6 text-gray-400 cursor-pointer hover:text-gray-600" 
                onClick={toggleSidebar}
              />
            </div>
          </div>
        </div>
      )}

      {/* Main Sidebar */}
      {!isCollapsed && (
        <div className={`w-70 bg-white border-r border-gray-200 flex flex-col transition-all duration-300 ease-in-out ${className || ''}`}>
            {/* Logo and Header */}
            <div className="p-6 border-b border-gray-100">
                <div className="flex items-center gap-2 mb-8">
                    <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center">
                        <HiOutlineMap className="w-5 h-5 text-white" />
                    </div>
                    <h1 className="font-semibold text-gray-900 flex-1">Roadmap AI</h1>
                    <LuPanelLeftClose 
                      className="w-6 h-6 text-gray-400 cursor-pointer hover:text-gray-600" 
                      onClick={toggleSidebar}
                    />
                </div>

                <button
                    onClick={() => setIsNewProjectOpen(true)}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md text-sm font-medium flex items-center justify-center gap-2 transition-colors cursor-pointer"
                    >
                    <FiPlus className="w-4 h-4" />
                    New Project
                </button>
            </div>

            {/* New Project Modal */}
            <NewProjectModal 
                isOpen={isNewProjectOpen}
                onClose={() => setIsNewProjectOpen(false)}
                onCreateProject={createProject}
            />

            {/* Projects List */}
            <div className="flex-1 overflow-hidden">
                    <div className="px-4 pt-4 pb-2">
                    <h2 className="text-sm font-semibold text-gray-500">
                        Projects ({projects.length})
                    </h2>
                </div>
                
                <div className="flex-1 px-5 overflow-y-auto">
                <div className="space-y-[2px]">
                    {projects.map((project) => (
                    <div
                        key={project.id}
                        onClick={() => selectProject(project.id)}
                        onContextMenu={(e) => handleRightClick(e, project)}
                        className={`px-3 py-2 rounded-lg cursor-pointer transition-all hover:bg-gray-50 border ${
                        currentProject?.id === project.id 
                            ? 'border-blue-200 bg-blue-50' 
                            : 'border-transparent'
                        }`}
                    >
                        <div className="flex items-start gap-2">
                            <div className="flex-shrink-0">
                                <FiFolder className="w-5 h-5 text-gray-400" />
                            </div>
                            <div className="flex-1 min-w-0">
                                {editingProject === project.id ? (
                                  <input
                                    type="text"
                                    value={editingName}
                                    onChange={(e) => setEditingName(e.target.value)}
                                    onBlur={cancelRename} // Revert to original name on blur
                                    onKeyDown={handleKeyDown}
                                    onFocus={(e) => e.target.select()} // Select all text on focus
                                    className="font-medium text-gray-900 text-sm bg-transparent border-none outline-none focus:bg-white focus:border focus:border-blue-500 focus:rounded px-1 w-full"
                                    autoFocus
                                  />
                                ) : (
                                  <h3 className="font-medium text-gray-900 text-sm truncate">{project.name}</h3>
                                )}
                            </div>
                        </div>
                    </div>
                    ))}
                </div>
                </div>
            </div>

            {/* User Profile */}
            <div className="p-4 border-t flex flex-col border-gray-100">
                <div className='flex items-center gap-2 p-3 rounded-lg hover:bg-gray-50 cursor-pointer'>
                    <HiOutlineMoon className='w-6 h-6' />
                    <p>Toggle Theme</p>
                </div>
                <div className="flex items-center gap-2 p-3 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center text-white">
                        <FiUser className="w-4 h-4" />
                    </div>
                    <div className="flex-1">
                        <p className="text-gray-900">John Doe</p>
                    </div>
                    <HiDotsHorizontal className="w-5 h-5 text-gray-400" />
                </div>
            </div>
        </div>
      )}

      <ProjectMenuModal 
        isOpen={contextMenu.show}
        x={contextMenu.x}
        y={contextMenu.y}
        project={contextMenu.project}
        onClose={closeContextMenu}
        onRename={startRename}
        onDelete={handleDelete}
      />
    </>
  );
};

export default Sidebar;