import React from 'react';
import { HiTrash, HiArrowUp } from 'react-icons/hi2';

const ArchivedTaskContextMenu = ({ isOpen, onClose, task, anchorRef, onDelete, onUnarchive }) => {
  if (!isOpen) return null;

  const getPosition = () => {
    if (!anchorRef) return { top: 0, right: 0 };

    const rect = anchorRef.getBoundingClientRect();
    const position = {
      top: rect.bottom + 4,
      right: window.innerWidth - rect.right
    };
    
    console.log('Context menu position:', position, 'Anchor rect:', rect);
    return position;
  };

  return (
    <div
      className="fixed inset-0 z-[9999]"
      onClick={onClose}
    >
      {/* Context Menu */}
      <div
        className="absolute bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-1 min-w-[160px]"
        style={getPosition()}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Menu Options */}
        <div className="py-1">
          <button
            onClick={() => {
              onUnarchive(task);
              onClose();
            }}
            className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] flex items-center gap-3"
          >
            <HiArrowUp className="w-4 h-4" />
            Unarchive
          </button>
          <button
            onClick={() => {
              onDelete(task);
              onClose();
            }}
            className="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center gap-3"
          >
            <HiTrash className="w-4 h-4" />
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default ArchivedTaskContextMenu;
