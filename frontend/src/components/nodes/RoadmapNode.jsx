import { Handle, Position } from '@xyflow/react';
import { FaCheckCircle, FaClock, FaPlay, FaExclamationTriangle } from 'react-icons/fa';

export const RoadmapNode = ({ data }) => {
  const nodeData = data;
  
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
        return 'border-green-200 bg-green-50';
      case 'in-progress':
        return 'border-blue-200 bg-blue-50';
      case 'pending':
        return 'border-gray-200 bg-gray-50';
      default:
        return 'border-yellow-200 bg-yellow-50';
    }
  };

  const getCategoryColor = () => {
    switch (nodeData.category) {
      case 'planning':
        return 'bg-purple-100 text-purple-800';
      case 'development':
        return 'bg-blue-100 text-blue-800';
      case 'testing':
        return 'bg-orange-100 text-orange-800';
      case 'deployment':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className={`bg-white border-2 rounded-lg p-4 min-w-[280px] max-w-[280px] shadow-sm hover:shadow-md transition-all ${getStatusColor()}`}>
      <Handle
        type="target"
        position={Position.Left}
        className="w-3 h-3 bg-gray-400 border-2 border-white"
      />
      
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <h3 className="font-semibold text-gray-900 text-sm leading-tight">{nodeData.title}</h3>
          {getStatusIcon()}
        </div>
        
        <p className="text-gray-600 text-xs leading-relaxed line-clamp-3">
          {nodeData.description}
        </p>
        
        <div className="flex items-center justify-between">
          <span className={`px-2 py-1 text-xs rounded-full font-medium ${getCategoryColor()}`}>
            {nodeData.category}
          </span>
          <span className="text-xs text-gray-500 font-medium">
            {nodeData.estimatedDays}d
          </span>
        </div>
      </div>
      
      <Handle
        type="source"
        position={Position.Right}
        className="w-3 h-3 bg-blue-500 border-2 border-white"
      />
    </div>
  );
};
