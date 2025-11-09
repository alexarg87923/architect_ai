import React, { useState, useEffect } from 'react';
import { FiX } from 'react-icons/fi';
import { HiDotsHorizontal } from 'react-icons/hi';
import ArchivedTaskContextMenu from './context_menus/ArchivedTaskContextMenu';

const ArchivedTasksModal = ({ isOpen, onClose, archivedTasks, sectionTitle, onDelete, onUnarchive }) => {
  const [isAnimating, setIsAnimating] = useState(false);
  const [contextMenu, setContextMenu] = useState({ show: false, task: null, anchorRef: null });

  useEffect(() => {
    if (isOpen) {
      // Small delay to ensure the element is rendered before starting animation
      setTimeout(() => setIsAnimating(true), 10);
    } else {
      setIsAnimating(false);
    }
  }, [isOpen]);

  const handleClose = () => {
    setIsAnimating(false);
    // Wait for animation to complete before calling onClose
    setTimeout(() => {
      onClose();
    }, 200);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      handleClose();
    }
  };

  const handleContextMenu = (e, task) => {
    e.preventDefault();
    e.stopPropagation();
    setContextMenu({ show: true, task, anchorRef: e.currentTarget });
  };

  const closeContextMenu = () => {
    setContextMenu({ show: false, task: null, anchorRef: null });
  };

  const handleDelete = (task) => {
    if (onDelete) {
      onDelete(task);
    }
  };

  const handleUnarchive = (task) => {
    if (onUnarchive) {
      onUnarchive(task);
    }
  };

  if (!isOpen) return null;

  return (
    <div 
      className={`fixed inset-0 bg-black/75 flex items-center justify-center z-50 transition-opacity duration-200 ${
        isAnimating ? 'opacity-100' : 'opacity-0'
      }`}
      onKeyDown={handleKeyDown}
      tabIndex={-1}
    >
      <div 
        className={`bg-white dark:bg-[#2a2a2a] border dark:border-[#3C3C3C] rounded-lg p-6 w-[500px] max-w-90vw max-h-[80vh] transition-all duration-200 ${
          isAnimating ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Archived Tasks - {sectionTitle}
          </h2>
          <button
            onClick={handleClose}
            className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <FiX className="w-5 h-5" />
          </button>
        </div>
        
        <div className="space-y-2 max-h-[400px] overflow-y-auto">
          {archivedTasks && archivedTasks.length > 0 ? (
            archivedTasks.map((task) => (
              <div
                key={task.id}
                className="flex items-center space-x-3 p-3 bg-gray-50 dark:bg-[#3A3A3A] rounded-lg border border-gray-200 dark:border-[#3C3C3C]"
              >
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                  task.completed
                    ? 'bg-green-500 border-green-500'
                    : 'border-gray-300 dark:border-gray-600'
                } cursor-not-allowed hover:opacity-80`}>
                  {task.completed && <span className="text-white text-xs">✓</span>}
                </div>
                <div className={`flex-1 text-sm ${
                  task.completed ? 'line-through text-gray-500' : 'text-gray-700 dark:text-gray-300'
                }`}>
                  {task.text}
                </div>
                <button
                  onClick={(e) => handleContextMenu(e, task)}
                  className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#4A4A4A] rounded transition-colors"
                >
                  <HiDotsHorizontal className="w-4 h-4" />
                </button>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500 dark:text-gray-400">
              <div className="text-sm">No archived tasks found</div>
            </div>
          )}
        </div>
        
        <div className="mt-6 flex justify-end">
          <button
            onClick={handleClose}
            className="px-4 py-2 bg-gray-200 dark:bg-gray-600 hover:bg-gray-300 dark:hover:bg-gray-500 text-gray-700 dark:text-gray-300 rounded-md text-sm font-medium transition-colors"
          >
            Close
          </button>
        </div>
      </div>
      
      {/* Context Menu */}
      <ArchivedTaskContextMenu
        isOpen={contextMenu.show}
        onClose={closeContextMenu}
        task={contextMenu.task}
        anchorRef={contextMenu.anchorRef}
        onDelete={handleDelete}
        onUnarchive={handleUnarchive}
      />
    </div>
  );
};

export default ArchivedTasksModal;
