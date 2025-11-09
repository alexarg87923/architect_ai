import { Handle, Position } from '@xyflow/react';
import { FaCheckCircle, FaClock, FaPlay, FaExclamationTriangle } from 'react-icons/fa';

export const RoadmapNode = ({ data }) => {
  const nodeData = data;
  
  const handleNodeClick = () => {
    // Only show modal for setup category nodes
    if (nodeData.category === 'setup' && nodeData.onOpenOverviewModal) {
      nodeData.onOpenOverviewModal(nodeData);
    }
  };
  
  const getStatusIcon = () => {
    switch (nodeData.status) {
      case 'completed':
        return <FaCheckCircle className="w-5 h-5 text-green-600" />;
      case 'in-progress':
        return <FaPlay className="w-5 h-5 text-blue-600" />;
      case 'pending':
        return <FaClock className="w-5 h-5 text-gray-400" />;
      default:
        return <FaExclamationTriangle className="w-5 h-5 text-yellow-600" />;
    }
  };

  const getStatusColor = () => {
    switch (nodeData.status) {
      case 'completed':
        return 'border-green-200 dark:border-green-700 bg-green-50 dark:bg-green-900/20';
      case 'in-progress':
        return 'border-blue-200 dark:border-blue-700 bg-blue-50 dark:bg-blue-900/20';
      case 'pending':
        return 'border-gray-200 dark:border-[#3c3c3c] bg-gray-50 dark:bg-[#2a2a2a]';
      default:
        return 'border-yellow-200 dark:border-yellow-700 bg-yellow-50 dark:bg-yellow-900/20';
    }
  };

  const getCategoryColor = () => {
    switch (nodeData.category) {
      case 'planning':
        return 'bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-300';
      case 'development':
        return 'bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300';
      case 'testing':
        return 'bg-orange-100 dark:bg-orange-900/30 text-orange-800 dark:text-orange-300';
      case 'deployment':
        return 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300';
      default:
        return 'bg-gray-100 dark:bg-gray-700/50 text-gray-800 dark:text-gray-300';
    }
  };

  return (
      <div 
        className={`bg-white dark:bg-[#2a2a2a] border-1 border-gray-300 dark:border-[#3c3c3c] rounded-xl p-4 min-w-[450px] max-w-[450px] h-[220px] shadow-sm hover:shadow-md transition-shadow ${getStatusColor()} ${nodeData.category === 'setup' ? 'cursor-pointer' : ''}`}
        onClick={handleNodeClick}
      >

      {/* Click indicator for setup node */}
      {nodeData.category === 'setup' && (
        <div className="absolute top-0 left-0 -translate-y-full text-sm px-2 py-1 font-mono font-semibold text-purple-400 dark:text-purple-400 drop-shadow-[0_0_8px_rgba(168,85,247,0.5)] dark:drop-shadow-[0_0_8px_rgba(196,181,253,0.6)]">
          Click for Overview
        </div>
      )}

      <Handle
        type="target"
        position={Position.Top}
        id="top"
      />
      
      {/* Left and Right handles for subtask connections */}
      <Handle
        type="source"
        position={Position.Left}
        id="left"
      />
      <Handle
        type="source"
        position={Position.Right}
        id="right"
      />
      
      <div className="flex flex-col h-full justify-between">
        <div className="space-y-3">
          <div className="flex items-start justify-between">
            <h3 className="font-semibold text-gray-900 dark:text-white text-lg leading-tight">{nodeData.title}</h3>
            {getStatusIcon()}
          </div>
          
          <p className="text-gray-500 dark:text-[#9f9f9f] text-md leading-relaxed line-clamp-3">
            {nodeData.description}
          </p>
        </div>
        
        <div className="space-y-2">
          {/* Progress and Subtasks Info */}
          {nodeData.subtasks && nodeData.subtasks.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-600 dark:text-gray-400">
                  {nodeData.subtasks.filter(st => st.completed).length}/{nodeData.subtasks.length} subtasks
                </span>
                <span className="text-gray-600 dark:text-gray-400">
                  {nodeData.completionPercentage || 0}%
                </span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${nodeData.completionPercentage || 0}%` }}
                />
              </div>
            </div>
          )}
          
          <div className="flex items-center justify-between">
            <span className={`px-2 py-1 text-sm rounded-full font-medium ${getCategoryColor()}`}>
              {nodeData.category}
            </span>
            <span className="text-sm text-gray-500 dark:text-[#9f9f9f] font-medium mt-1">
              {nodeData.estimatedDays}d
            </span>
          </div>
        </div>
      </div>
      
        <Handle
          type="source"
          position={Position.Bottom}
          id="bottom"
        />
      </div>
  );
};
