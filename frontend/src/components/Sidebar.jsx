import React, { useState, useEffect } from 'react';
import { FiPlus, FiFolder, FiUser } from 'react-icons/fi';
import { HiOutlineMap, HiOutlineMoon, HiDotsHorizontal, HiOutlineSun } from 'react-icons/hi';
import NewProjectModal from './modals/NewProjectModal';
import ProjectMenuModal from './modals/ProjectMenuModal';
import ProfileMenuModal from './modals/ProfileMenuModal';
import SettingsModal from './modals/SettingsModal';
import { LuPanelLeftClose, LuPanelLeftOpen } from "react-icons/lu";
import { useProjects } from '../hooks/useProjects';
import { useSelectedProject } from '../contexts/SelectedProjectContext';
import { useAuth } from '../contexts/AuthContext';


const Sidebar = ({ isDark, toggleTheme, isCollapsed, setIsCollapsed }) => {
  // Use useProjects for project data management
  const { projects, createProject, updateProject, deleteProject } = useProjects();
  
  // Use context for selected project state
  const { selectedProject, selectProject, clearSelection } = useSelectedProject();

  // Use auth context for user data
  const { user, logout } = useAuth();

  const [isNewProjectOpen, setIsNewProjectOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [contextMenu, setContextMenu] = useState({ show: false, x: 0, y: 0, project: null });
  const [editingProject, setEditingProject] = useState(null);
  const [editingName, setEditingName] = useState('');
  const [originalName, setOriginalName] = useState('');

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
    updateProject(projectId, { name: newName });
  };

  const startRename = (project) => {
    selectProject(project); // Select the project being renamed using context
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
    deleteProject(projectId); // Use the hook's delete function
    // Clear selection if the deleted project was selected
    if (selectedProject?.id === projectId) {
      clearSelection();
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const toggleUserMenu = () => {
    setShowUserMenu(!showUserMenu);
  };

  const closeUserMenu = () => {
    setShowUserMenu(false);
  };

  const openSettings = () => {
    setIsSettingsOpen(true);
  };

  const closeSettings = () => {
    setIsSettingsOpen(false);
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
              <h1 className="font-semibold text-gray-900 dark:text-gray-100 flex-1">Roadmap AI</h1>
              <LuPanelLeftOpen 
                className="w-6 h-6 text-gray-400 dark:text-gray-300 cursor-pointer hover:text-gray-600 dark:hover:text-gray-100" 
                onClick={toggleSidebar}
              />
            </div>
          </div>
        </div>
      )}

      {/* Main Sidebar */}
      {!isCollapsed && (
        <div className='w-70 bg-white dark:bg-[#2a2a2a] border-r border-gray-200 dark:border-[#3C3C3C] flex flex-col transition-all duration-300 ease-in-out'>
            {/* Logo and Header */}
            <div className="p-6 border-b border-gray-100 dark:border-[#3C3C3C]">
                <div className="flex items-center gap-2 mb-8">
                    <div className="w-7 h-7 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center">
                        <HiOutlineMap className="w-5 h-5 text-white" />
                    </div>
                    <h1 className="font-semibold text-gray-900 dark:text-gray-100 flex-1">Roadmap AI</h1>
                    <LuPanelLeftClose 
                      className="w-6 h-6 text-gray-400 dark:text-gray-300 cursor-pointer hover:text-gray-600 dark:hover:text-gray-100" 
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
                    <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400">
                        Projects ({projects.length})
                    </h2>
                </div>
                
                <div className="flex-1 px-5 overflow-y-auto">
                <div className="space-y-[2px]">
                    {projects.map((project) => (
                    <div
                        key={project.id}
                        onClick={() => selectProject(project)}
                        onContextMenu={(e) => handleRightClick(e, project)}
                        className={`px-3 py-2 rounded-lg cursor-pointer transition-all hover:bg-gray-50 dark:hover:bg-[#3A3A3A] border ${
                        selectedProject?.id === project.id 
                            ? 'border-blue-200 dark:border-blue-500 bg-blue-50 dark:bg-[#1e3a5f]' 
                            : 'border-transparent'
                        }`}
                    >
                        <div className="flex items-start gap-2">
                            <div className="flex-shrink-0">
                                <FiFolder className="w-5 h-5 text-gray-400 dark:text-gray-500" />
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
                                    className="font-medium text-gray-900 dark:text-gray-100 text-sm bg-transparent border-none outline-none focus:bg-white dark:focus:bg-[#3A3A3A] focus:border focus:border-blue-500 focus:rounded px-1 w-full"
                                    autoFocus
                                  />
                                ) : (
                                  <h3 className="font-medium text-gray-900 dark:text-gray-100 text-sm truncate">{project.name}</h3>
                                )}
                            </div>
                        </div>
                    </div>
                    ))}
                </div>
                </div>
            </div>

            {/* User Profile */}
            <div className="p-4 border-t border-gray-100 dark:border-[#3C3C3C] flex flex-col">
                <button className='flex items-center gap-2 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-[#3A3A3A] cursor-pointer transition-colors' onClick={toggleTheme}>
                  {isDark ? (
                      <HiOutlineSun className="w-6 h-6 text-gray-700 dark:text-gray-300" />
                    ) : (
                      <HiOutlineMoon className="w-6 h-6 text-gray-700 dark:text-gray-300" />
                  )}
                  <p className="text-gray-700 dark:text-gray-300">Toggle Theme</p>
                </button>
                
                {/* User Profile with Popup Menu */}
                <div className="relative user-menu-container">
                    <div 
                        className="flex items-center gap-2 p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-[#3A3A3A] cursor-pointer"
                        onClick={toggleUserMenu}
                    >
                        <div className="w-6 h-6 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center text-white">
                            <FiUser className="w-4 h-4" />
                        </div>
                        <div className="flex-1">
                            <p className="text-gray-900 dark:text-gray-100">
                                {user ? `${user.first_name} ${user.last_name}` : 'Loading...'}
                            </p>
                        </div>
                        <HiDotsHorizontal className="w-5 h-5 text-gray-400 dark:text-gray-500" />
                    </div>

                    {/* Profile Menu Modal */}
                    <ProfileMenuModal 
                        isOpen={showUserMenu}
                        user={user}
                        onClose={closeUserMenu}
                        onLogout={handleLogout}
                        onOpenSettings={openSettings}
                    />
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

      {/* Settings Modal */}
      <SettingsModal 
        isOpen={isSettingsOpen}
        onClose={closeSettings}
      />
    </>
  );
};

export default Sidebar;