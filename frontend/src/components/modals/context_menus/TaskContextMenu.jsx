import React, { useEffect } from 'react';
import { HiMiniPencilSquare } from "react-icons/hi2";
import { HiOutlineTrash, HiArchive } from "react-icons/hi";

const TaskContextMenu = ({ isOpen, x, y, task, sectionKey, onClose, onRename, onDelete, onArchive }) => {

  // Close context menu when clicking outside
  useEffect(() => {
    const handleClickOutside = () => {
      if (isOpen) {
        onClose();
      }
    };
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [isOpen, onClose]);

  if (!isOpen || !task) return null;

  return (
    <div 
      className="fixed inset-0 z-50"
      onClick={onClose}
    >
      <div
        className="absolute bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-2 min-w-[160px]"
        style={{ left: x, top: y }}
        onClick={e => e.stopPropagation()}
      >
        <button
          onClick={() => onRename(sectionKey, task)}
          className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] flex items-center gap-3"
        >
          <HiMiniPencilSquare className="w-4 h-4" />
          Rename
        </button>
        {/* NEED TO IMPLEMENT */}
        <button
          onClick={() => onArchive(sectionKey, task)}
          className="w-full px-4 py-2 text-left text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] flex items-center gap-3"
        >
          <HiArchive className="w-4 h-4" />
          Archive
        </button>
        <button
          onClick={() => onDelete(sectionKey, task)}
          className="w-full px-4 py-2 text-left text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 flex items-center gap-3"
        >
          <HiOutlineTrash className="w-4 h-4" />
          Move to Trash
        </button>
      </div>
    </div>
  );
};

export default TaskContextMenu;
