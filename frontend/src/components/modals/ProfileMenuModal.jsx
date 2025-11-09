import React from 'react';
import { HiLogout } from 'react-icons/hi';
import { FiUser } from 'react-icons/fi';

const ProfileMenuModal = ({ isOpen, user, onClose, onLogout }) => {
  if (!isOpen) return null;

  const handleLogout = () => {
    onLogout();
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
      <div className="absolute bottom-full left-0 right-0 mb-2 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-2 z-50">
        {/* User Info Header */}
        <div className="px-4 py-3 border-b border-gray-100 dark:border-[#3C3C3C]">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-md flex items-center justify-center text-white">
              <FiUser className="w-5 h-5" />
            </div>
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100 text-sm">
                {user ? `${user.first_name} ${user.last_name}` : 'User'}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">{user?.email}</p>
            </div>
          </div>
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

export default ProfileMenuModal;
