import React, { useState, useEffect } from 'react';
import { RxCross2 } from "react-icons/rx";
import { FaRegKeyboard } from "react-icons/fa";
import { FaEye, FaEyeSlash } from "react-icons/fa";
import ApiClient from '../../services/api';

const SettingsModal = ({ isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState('account');
  const [userData, setUserData] = useState({
    name: '',
    email: '',
    createdAt: '',
    lastActive: ''
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [passwordMessage, setPasswordMessage] = useState({ type: '', text: '' });
  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false
  });
  const [feedbackMessage, setFeedbackMessage] = useState({ type: '', text: '' });
  const [activityMetrics, setActivityMetrics] = useState({
    totalProjects: 0,
    roadmapsGenerated: 0,
    activeProjects: 0,
    completionRate: 0
  });
  const [loading, setLoading] = useState(false);
  const [feedbackData, setFeedbackData] = useState({
    message: '',
    type: 'general'
  });

  // Fetch user data and metrics when modal opens
  useEffect(() => {
    if (isOpen) {
      fetchUserData();
      fetchActivityMetrics();
    }
  }, [isOpen]);

  const fetchUserData = async () => {
    try {
      setLoading(true);
      // TODO: Replace with actual API call when backend is ready
      // const userData = await ApiClient.getUserProfile();
      // setUserData(userData);
      
      // Mock data for now
      setUserData({
        name: 'John Doe',
        email: 'johndoe@example.com',
        createdAt: '2024-01-15',
        lastActive: '2024-07-28'
      });
    } catch (error) {
      console.error('Failed to fetch user data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchActivityMetrics = async () => {
    try {
      // TODO: Replace with actual API call when backend is ready
      // const metrics = await ApiClient.getUserMetrics();
      // setActivityMetrics(metrics);
      
      // Mock data for now
      setActivityMetrics({
        totalProjects: 5,
        roadmapsGenerated: 3,
        activeProjects: 2,
        completionRate: 60
      });
    } catch (error) {
      console.error('Failed to fetch activity metrics:', error);
    }
  };

  const handleSaveProfile = async () => {
    try {
      setLoading(true);
      // TODO: Replace with actual API call when backend is ready
      // await ApiClient.updateUserProfile(userData);
      console.log('Profile updated successfully');
    } catch (error) {
      console.error('Failed to update profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitFeedback = async () => {
    // Frontend validation
    if (!feedbackData.message.trim()) {
      setFeedbackMessage({ type: 'error', text: 'Please enter a message before submitting feedback.' });
      setTimeout(() => setFeedbackMessage({ type: '', text: '' }), 3000);
      return;
    }

    try {
      setLoading(true);
      await ApiClient.submitFeedback(feedbackData.type, feedbackData.message);
      console.log('Feedback submitted successfully');
      setFeedbackData({ message: '', type: 'general' });
      setFeedbackMessage({ type: 'success', text: 'Feedback submitted successfully!' });
      // Clear message after 3 seconds
      setTimeout(() => setFeedbackMessage({ type: '', text: '' }), 3000);
    } catch (error) {
      console.error('Failed to submit feedback:', error);
      let errorMessage = 'Failed to submit feedback';
      if (error.message.includes('HTTP 400')) {
        errorMessage = 'Invalid feedback data. Please check your input.';
      } else if (error.message.includes('HTTP 404')) {
        errorMessage = 'User not found';
      } else if (error.message.includes('HTTP 500')) {
        errorMessage = 'Server error occurred while submitting feedback';
      }
      setFeedbackMessage({ type: 'error', text: errorMessage });
      // Clear message after 5 seconds
      setTimeout(() => setFeedbackMessage({ type: '', text: '' }), 5000);
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async () => {
    // Clear any previous messages
    setPasswordMessage({ type: '', text: '' });
    
    if (!passwordData.currentPassword.trim()) {
      setPasswordMessage({ type: 'error', text: 'Current password is required' });
      return;
    }
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setPasswordMessage({ type: 'error', text: 'New password and confirm password do not match' });
      return;
    }
    
    if (passwordData.newPassword.length < 6) {
      setPasswordMessage({ type: 'error', text: 'Password must be at least 6 characters long' });
      return;
    }
    
    setLoading(true);
    try {
      const response = await ApiClient.changePassword(
        passwordData.currentPassword,
        passwordData.newPassword,
        passwordData.confirmPassword
      );
      
      if (response.success) {
        setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
        setPasswordMessage({ type: 'success', text: 'Password changed successfully!' });
      }
    } catch (error) {
      console.error('Failed to change password:', error);
      // Extract error message from the response
      let errorMessage = 'Failed to change password';
      
      if (error.message.includes('HTTP 400')) {
        if (error.message.includes('Current password is incorrect')) {
          errorMessage = 'Current password is incorrect';
        } else if (error.message.includes('Current password is required')) {
          errorMessage = 'Current password is required';
        } else if (error.message.includes('do not match')) {
          errorMessage = 'New password and confirm password do not match';
        } else if (error.message.includes('at least 6 characters')) {
          errorMessage = 'Password must be at least 6 characters long';
        }
      } else if (error.message.includes('HTTP 404')) {
        errorMessage = 'User not found';
      } else if (error.message.includes('HTTP 500')) {
        errorMessage = 'Server error occurred while changing password';
      }
      
      setPasswordMessage({ type: 'error', text: errorMessage });
    } finally {
      setLoading(false);
    }
  };

  const tabs = [
    { id: 'account', label: 'Account' },
    { id: 'feedback', label: 'Feedback' },
    { id: 'hotkeys', label: 'Hotkeys' }
  ];

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/75 flex items-center justify-center z-60">
      <div className="bg-white dark:bg-[#2a2a2a] rounded-lg shadow-xl w-[800px] h-[600px] flex">
        {/* Left Sidebar - Tabs */}
        <div className="w-48 bg-gray-50 dark:bg-[#1a1a1a] rounded-l-lg border-r border-gray-200 dark:border-[#3C3C3C] flex flex-col py-4">
          <div className="flex-1 p-4">
            <nav className="space-y-1">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-left px-3 py-2 text-sm rounded-md transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 font-medium'
                      : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A]'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Right Content Area */}
        <div className="flex-1 flex flex-col">
          {/* Header with just close button */}
          <div className="flex items-center justify-end px-2 py-2">
            <button
              onClick={onClose}
              className="p-1 rounded-full hover:bg-gray-200 dark:hover:bg-[#3A3A3A] text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors cursor-pointer"
            >
              <RxCross2 className="w-5 h-5" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto p-6 pt-4">
            {activeTab === 'account' && (
              <div className="space-y-6">
                {/* Activity Metrics Section */}
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Activity & Progress</h3>
                  <div className="grid grid-cols-2 gap-3">
                    <div className="bg-gray-50 dark:bg-[#1a1a1a] p-3 rounded-lg">
                      <div className="text-lg font-bold text-blue-600 dark:text-blue-400">{activityMetrics.totalProjects}</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Total Projects</div>
                    </div>
                    <div className="bg-gray-50 dark:bg-[#1a1a1a] p-3 rounded-lg">
                      <div className="text-lg font-bold text-green-600 dark:text-green-400">{activityMetrics.roadmapsGenerated}</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Roadmaps Generated</div>
                    </div>
                    <div className="bg-gray-50 dark:bg-[#1a1a1a] p-3 rounded-lg">
                      <div className="text-lg font-bold text-orange-600 dark:text-orange-400">{activityMetrics.activeProjects}</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Active Projects</div>
                    </div>
                    <div className="bg-gray-50 dark:bg-[#1a1a1a] p-3 rounded-lg">
                      <div className="text-lg font-bold text-purple-600 dark:text-purple-400">{activityMetrics.completionRate}%</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Completion Rate</div>
                    </div>
                  </div>
                </div>

                {/* Profile Section */}
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">
                    Profile
                    <span className="ml-2 text-xs text-gray-500 dark:text-gray-400 font-normal">(unchangeable in beta)</span>
                  </h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Name
                      </label>
                      <input
                        type="text"
                        value={userData.name}
                        onChange={(e) => setUserData({ ...userData, name: e.target.value })}
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your name"
                      />
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Email
                      </label>
                      <input
                        type="email"
                        value={userData.email}
                        onChange={(e) => setUserData({ ...userData, email: e.target.value })}
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Enter your email"
                      />
                    </div>

                    <button
                      onClick={handleSaveProfile}
                      disabled={true}
                      className="px-3 py-1.5 text-xs bg-gray-400 text-white rounded-md cursor-not-allowed transition-colors"
                    >
                      Save Changes
                    </button>
                  </div>
                </div>

                {/* Password Change Section */}
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Change Password</h3>
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Current Password
                      </label>
                      <div className="relative">
                        <input
                          type={showPasswords.current ? "text" : "password"}
                          value={passwordData.currentPassword}
                          onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                          className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-8"
                          placeholder="Enter current password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPasswords({ ...showPasswords, current: !showPasswords.current })}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        >
                          {showPasswords.current ? <FaEyeSlash className="w-3 h-3" /> : <FaEye className="w-3 h-3" />}
                        </button>
                      </div>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        New Password
                      </label>
                      <div className="relative">
                        <input
                          type={showPasswords.new ? "text" : "password"}
                          value={passwordData.newPassword}
                          onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                          className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-8"
                          placeholder="Enter new password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPasswords({ ...showPasswords, new: !showPasswords.new })}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        >
                          {showPasswords.new ? <FaEyeSlash className="w-3 h-3" /> : <FaEye className="w-3 h-3" />}
                        </button>
                      </div>
                    </div>
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Confirm New Password
                      </label>
                      <div className="relative">
                        <input
                          type={showPasswords.confirm ? "text" : "password"}
                          value={passwordData.confirmPassword}
                          onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                          className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 pr-8"
                          placeholder="Confirm new password"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPasswords({ ...showPasswords, confirm: !showPasswords.confirm })}
                          className="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                        >
                          {showPasswords.confirm ? <FaEyeSlash className="w-3 h-3" /> : <FaEye className="w-3 h-3" />}
                        </button>
                      </div>
                    </div>

                    {/* Flash Message */}
                    {passwordMessage.text && (
                      <div className={`px-3 py-2 rounded-md text-xs ${
                        passwordMessage.type === 'success' 
                          ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800'
                          : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800'
                      }`}>
                        {passwordMessage.text}
                      </div>
                    )}

                    <button
                      onClick={handleChangePassword}
                      disabled={loading}
                      className="px-3 py-1.5 text-xs bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {loading ? 'Changing Password...' : 'Change Password'}
                    </button>
                  </div>
                </div>

                {/* Account Info Section */}
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Account Information</h3>
                  <div className="space-y-1 text-xs text-gray-600 dark:text-gray-400">
                    <div>Account created: {userData.createdAt}</div>
                    <div>Last active: {userData.lastActive}</div>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'feedback' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Send Feedback</h3>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mb-3">
                    Help us improve by sharing your thoughts, suggestions, or reporting issues.
                  </p>
                  
                  <div className="space-y-3">
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Feedback Type
                      </label>
                      <select
                        value={feedbackData.type}
                        onChange={(e) => {
                          setFeedbackData({ ...feedbackData, type: e.target.value });
                          // Clear any existing message when user changes type
                          if (feedbackMessage.text) {
                            setFeedbackMessage({ type: '', text: '' });
                          }
                        }}
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="general">General Feedback</option>
                        <option value="bug">Bug Report</option>
                        <option value="feature">Feature Request</option>
                        <option value="improvement">Improvement Suggestion</option>
                      </select>
                    </div>
                    
                    <div>
                      <label className="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                        Message
                      </label>
                      <textarea
                        value={feedbackData.message}
                        onChange={(e) => {
                          setFeedbackData({ ...feedbackData, message: e.target.value });
                          // Clear any existing message when user starts typing
                          if (feedbackMessage.text) {
                            setFeedbackMessage({ type: '', text: '' });
                          }
                        }}
                        rows="6"
                        className="w-full px-2 py-1.5 text-xs border border-gray-300 dark:border-[#3C3C3C] rounded-md bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Tell us what you think..."
                      />
                    </div>
                    
                    {/* Feedback Flash Message */}
                    {feedbackMessage.text && (
                      <div className={`px-3 py-2 rounded-md text-xs ${
                        feedbackMessage.type === 'success' 
                          ? 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-800'
                          : 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400 border border-red-200 dark:border-red-800'
                      }`}>
                        {feedbackMessage.text}
                      </div>
                    )}
                    
                    <button
                      onClick={handleSubmitFeedback}
                      disabled={loading || !feedbackData.message.trim()}
                      className="px-3 py-1.5 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                      {loading ? 'Sending...' : 'Send Feedback'}
                    </button>
                  </div>
                </div>

                {/* Help Section */}
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Help & Support</h3>
                  <div className="space-y-3">
                    <button className="w-full text-left p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg hover:bg-gray-100 dark:hover:bg-[#3A3A3A] transition-colors">
                      <div className="font-medium text-xs text-gray-900 dark:text-gray-100">Documentation</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Learn how to use the platform</div>
                    </button>
                    <button className="w-full text-left p-3 bg-gray-50 dark:bg-[#1a1a1a] rounded-lg hover:bg-gray-100 dark:hover:bg-[#3A3A3A] transition-colors">
                      <div className="font-medium text-xs text-gray-900 dark:text-gray-100">Contact Support</div>
                      <div className="text-xs text-gray-600 dark:text-gray-400">Get help from our team</div>
                    </button>
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'hotkeys' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mb-3 pb-2 border-b border-gray-200 dark:border-[#3C3C3C]">Keyboard Shortcuts</h3>
                  <div className="flex items-center justify-center py-12">
                    <div className="text-center">
                      <div className="flex justify-center mb-4">
                        <FaRegKeyboard className="text-4xl text-gray-400 dark:text-gray-500" />
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400 mb-2">Coming Soon</div>
                      <div className="text-xs text-gray-500 dark:text-gray-500">Keyboard shortcuts will be available in a future update</div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsModal; 