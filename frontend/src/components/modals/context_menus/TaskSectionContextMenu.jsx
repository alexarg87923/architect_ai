import React from 'react';
import { HiEye } from "react-icons/hi2";

const TaskSectionContextMenu = ({ isOpen, onClose, onViewArchive, anchorRef }) => {
  if (!isOpen) return null;

  const getPosition = () => {
    if (!anchorRef?.current) return { top: 0, right: 0 };

    const rect = anchorRef.current.getBoundingClientRect();
    return {
      top: rect.bottom + 4,
      right: window.innerWidth - rect.right
    };
  };

  return (
    <div
      className="fixed inset-0 z-40"
      onClick={onClose}
    >
      {/* Section Menu */}
      <div
        className="absolute bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-1 min-w-[160px] z-50"
        style={getPosition()}
      >
        {/* Menu Options */}
        <div className="py-1">
          <button
            onClick={onViewArchive}
            className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] flex items-center gap-3"
          >
            <HiEye className="w-4 h-4" />
            View Archive
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskSectionContextMenu;
