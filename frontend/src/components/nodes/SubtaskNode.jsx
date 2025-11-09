import React, { useState } from 'react';
import { Handle, Position } from '@xyflow/react';
import { FaCheckCircle, FaClock } from 'react-icons/fa';
import { EditNodeSidebar } from '../EditNodeSidebar';

export const SubtaskNode = ({ data }) => {
  const { subtask, onToggleComplete, parentNodeId } = data;
  const [isEditNodeSidebarOpen, setIsEditNodeSidebarOpen] = useState(false);
  
  const handleToggleComplete = () => {
    if (onToggleComplete) {
      onToggleComplete(parentNodeId, subtask.id, !subtask.completed);
    }
  };

  const getStatusIcon = () => {
    if (subtask.completed) {
      return <FaCheckCircle className="w-4 h-4 text-green-600" />;
    }
    return <FaClock className="w-4 h-4 text-gray-400" />;
  };

  const getNodeStyle = () => {
    if (subtask.completed) {
      return 'dark:border-green-700 bg-green-50 dark:bg-green-900/20';
    }
    return 'dark:border-[#3c3c3c] bg-white dark:bg-[#2a2a2a]';
  };

  const handleToggleNodeEditSidebar = () => {
    setIsEditNodeSidebarOpen((prevState) => !prevState);
  };

  const handleCloseEditNodeSidebar = () => {
    
  };

  const handleDeleteEditNodeSidebar = () => {
    
  };

  const handleUpdateEditNodeSidebar = () => {
    
  };

  return (
    <>
      <div
        className={`
          rounded-lg p-3 min-w-[280px] max-w-[280px] shadow-sm hover:shadow-md border-1
          transition-all cursor-pointer 
          ${getNodeStyle()} 
          ${isEditNodeSidebarOpen ? 'border-blue-500 dark:bg-blue-900/20' : subtask.completed ? 'border-green-200' : 'border-gray-200 border-1'}
        `}
      >
        {/* Left and Right handles for connections from roadmap nodes */}
        <Handle type="target" position={Position.Left} id="left" />
        <Handle type="target" position={Position.Right} id="right" />

        <div className="flex items-start space-x-3" onClick={handleToggleNodeEditSidebar}>
          <button
            className="mt-0.5 flex-shrink-0"
            onClick={(e) => {
              e.stopPropagation();
              handleToggleComplete();
            }}
          >
            {subtask.completed ? (
              <FaCheckCircle className="w-5 h-5 text-green-600 hover:text-green-700 transition-colors" />
            ) : (
              <div className="w-5 h-5 border-2 border-gray-300 dark:border-gray-600 rounded-full hover:border-green-500 transition-colors" />
            )}
          </button>

          <div className="flex-1 space-y-2">
            <h4
              className={`font-medium text-sm leading-tight ${
                subtask.completed
                  ? "text-gray-500 dark:text-gray-400 line-through"
                  : "text-gray-900 dark:text-white"
              }`}
            >
              {subtask.title}
            </h4>

            <p
              className={`text-xs leading-relaxed ${
                subtask.completed
                  ? "text-gray-400 dark:text-gray-500 line-through"
                  : "text-gray-600 dark:text-[#9f9f9f]"
              }`}
            >
              {subtask.description}
            </p>

            {subtask.estimated_hours && (
              <div className="flex items-center justify-between">
                <span
                  className={`text-xs font-medium ${
                    subtask.completed
                      ? "text-gray-400 dark:text-gray-500"
                      : "text-gray-500 dark:text-[#9f9f9f]"
                  }`}
                >
                  {subtask.estimated_hours}h
                </span>
                {getStatusIcon()}
              </div>
            )}
          </div>
        </div>
      </div>

      <EditNodeSidebar
        node={subtask}
        isOpen={isEditNodeSidebarOpen}
        onClose={handleCloseEditNodeSidebar}
        onDelete={handleDeleteEditNodeSidebar}
        onUpdate={handleUpdateEditNodeSidebar}
      />
    </>
  );
};
