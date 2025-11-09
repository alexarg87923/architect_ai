import React from 'react';
import { HiLogout } from 'react-icons/hi';
import { FiSettings } from 'react-icons/fi';

const ProfileContextMenu = ({ isOpen, onClose, onLogout, onOpenSettings }) => {
  if (!isOpen) return null;

  const handleLogout = () => {
    onLogout();
    onClose();
  };

  const handleSettings = () => {
    onOpenSettings();
    onClose();
  };

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 z-40" 
        onClick={onClose}
      />
      
      {/* Profile Menu */}
      <div className="absolute bottom-full left-0 right-0 mb-2 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-1 z-50">
        {/* User Info Header */}
        <div className="py-1 border-b border-gray-100 dark:border-[#3C3C3C]">
          <button
              onClick={handleSettings}
              className="w-full flex items-center gap-3 px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-[#3A3A3A] transition-colors"
            >
              <FiSettings className="w-4 h-4" />
              Settings
          </button>
        </div>
        
        {/* Menu Options */}
        <div className="py-1">
          <button
            onClick={handleLogout}
            className="w-full flex items-center gap-3 px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
          >
            <HiLogout className="w-4 h-4" />
            Sign out
          </button>
        </div>
      </div>
    </>
  );
};

export default ProfileContextMenu;
