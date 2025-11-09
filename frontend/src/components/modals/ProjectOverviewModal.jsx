import React, { useState, useEffect } from 'react';
import { FaTimes, FaRocket, FaClipboardList, FaClock, FaCheckCircle } from 'react-icons/fa';

export const ProjectOverviewModal = ({ isOpen, onClose, nodeData }) => {
  const [isAnimating, setIsAnimating] = useState(false);

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

  if (!isOpen) return null;

  // Use the overview from nodeData if available, otherwise fallback to default message
  const projectOverview = nodeData?.overview || ["Overview not present in Setup Node",];

  return (
    <div 
      className={`fixed inset-0 bg-black/75 flex items-center justify-center z-50 p-4 transition-opacity duration-200 ${
        isAnimating ? 'opacity-100' : 'opacity-0'
      }`}
      onClick={handleClose}
      onKeyDown={handleKeyDown}
      tabIndex={-1}
    >
      <div 
        className={`bg-white dark:bg-[#2a2a2a] border dark:border-[#3C3C3C] rounded-xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto transition-all duration-200 ${
          isAnimating ? 'opacity-100 scale-100' : 'opacity-0 scale-95'
        }`}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-[#3c3c3c]">
          <div className="flex items-center space-x-3">
            <FaRocket className="w-6 h-6 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Project Overview & Strategy
            </h2>
          </div>
          <button
            onClick={handleClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            <FaTimes className="w-5 h-5 text-gray-500 dark:text-gray-400" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Setup Node Description */}
          <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-300 mb-2 flex items-center">
              <FaCheckCircle className="w-5 h-5 mr-2" />
              {nodeData.title}
            </h3>
            <p className="text-blue-800 dark:text-blue-200">
              {nodeData.description}
            </p>
          </div>

          {/* Development Strategy */}
          <div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <FaClipboardList className="w-5 h-5 mr-2 text-green-600" />
              Development Strategy
            </h3>
            <div className="space-y-3">
              {projectOverview.map((strategy, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-full flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </div>
                  <p className="text-gray-700 dark:text-gray-300">{strategy}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Call to Action */}
          <div className="bg-gradient-to-r from-blue-50 to-green-50 dark:from-blue-900/20 dark:to-green-900/20 rounded-lg p-4">
            <p className="text-gray-800 dark:text-gray-200 text-center">
              <strong>Ready to get started?</strong> Complete the project setup to build momentum and start coding immediately! 🚀
            </p>
          </div>
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-gray-200 dark:border-[#3c3c3c] flex justify-end">
          <button
            onClick={handleClose}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
          >
            Let's Build This!
          </button>
        </div>
      </div>
    </div>
  );
};
