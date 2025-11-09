import React, { useState, useRef, useEffect, useContext } from 'react';
import { FaCircleArrowUp, FaMicrophone, FaChevronDown, FaRobot } from "react-icons/fa6";
import { RxCross2 } from "react-icons/rx";
import { BiSolidFaceMask } from "react-icons/bi";
import ApiClient from '../services/api';
import { useSelectedProject } from '../contexts/SelectedProjectContext';
import { useProjects } from '../hooks/useProjects';

const Agent = () => {
  const { selectedProject, updateSelectedProject } = useSelectedProject();
  const { refreshProjects } = useProjects();
  const [isOpen, setIsOpen] = useState(false);
  const [showActionMenu, setShowActionMenu] = useState(false);
  const [selectedAction, setSelectedAction] = useState('Chat');
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [conversationState, setConversationState] = useState(null);
  const [error, setError] = useState(null);
  const [currentPhase, setCurrentPhase] = useState('discovery');
  const [hasShownWelcome, setHasShownWelcome] = useState(false);
  const [isSimulating, setIsSimulating] = useState(false);
  const [selectedProjectType, setSelectedProjectType] = useState('codementor');
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const actionMenuRef = useRef(null);

  const actionOptions = [
    { id: 'Chat', label: 'Chat', description: 'General conversation' },
    { id: 'Edit', label: 'Edit', description: 'Edit specific node' },
    { id: 'Expand', label: 'Expand', description: 'Expand from node' },
    { id: 'Crawl', label: 'Crawl', description: 'Crawl specific resource' }
  ];

  const [availableProjectTypes, setAvailableProjectTypes] = useState([]);
  const [loadingProjectOptions, setLoadingProjectOptions] = useState(false);
  const [showProjectTypeMenu, setShowProjectTypeMenu] = useState(false);
  const projectTypeMenuRef = useRef(null);

  // Auto-scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Focus input when chat opens
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
      
      // Show welcome message on first open
      if (!hasShownWelcome) {
        setHasShownWelcome(true);
        const welcomeMessage = {
          id: Date.now(),
          type: 'agent',
          content: "Hi! I'm your AI Project Manager. I will create a roadmap for your project to help your ideas come to life. To get started give me a description of your project.",
          timestamp: new Date()
        };
        setMessages([welcomeMessage]);
      }
    }
  }, [isOpen, hasShownWelcome]);

  // Adjust textarea height when input value changes
  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  // Fetch available project types when component mounts
  useEffect(() => {
    const fetchProjectOptions = async () => {
      try {
        setLoadingProjectOptions(true);
        const result = await ApiClient.getProjectOptions();
        if (result.success && result.projectOptions) {
          setAvailableProjectTypes(result.projectOptions);
        }
      } catch (error) {
        console.error('Failed to fetch project options:', error);
        // Fallback to default options if API fails
        setAvailableProjectTypes([
          { value: 'codementor', label: 'CodeMentor' },
          { value: 'taskflow', label: 'TaskFlow' },
          { value: 'healthtracker', label: 'HealthTracker' }
        ]);
      } finally {
        setLoadingProjectOptions(false);
      }
    };

    fetchProjectOptions();
  }, []);

  // Close action menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (actionMenuRef.current && !actionMenuRef.current.contains(event.target)) {
        setShowActionMenu(false);
      }
      if (projectTypeMenuRef.current && !projectTypeMenuRef.current.contains(event.target)) {
        setShowProjectTypeMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  const handleActionSelect = (actionId) => {
    setSelectedAction(actionId);
    setShowActionMenu(false);
  };

  const handleProjectTypeSelect = (projectType) => {
    setSelectedProjectType(projectType);
    setShowProjectTypeMenu(false);
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsTyping(true);
    setError(null);
    
    // Reset textarea height after sending
    setTimeout(() => {
      if (inputRef.current) {
        inputRef.current.style.height = 'auto';
      }
    }, 0);

    try {
      // Call the real agent API
      const response = await ApiClient.chatWithAgent(
        userMessage.content,
        sessionId,
        selectedAction.toLowerCase(),
        conversationState
      );

      // Update session and conversation state
      if (response.sessionId) {
        setSessionId(response.sessionId);
      }
      if (response.conversationState) {
        setConversationState(response.conversationState);
        // Update current phase
        if (response.conversationState.phase) {
          setCurrentPhase(response.conversationState.phase);
        }
      }

      // Add agent response to messages
      const agentResponse = {
        id: Date.now() + 1,
        type: 'agent',
        content: response.agentResponse,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, agentResponse]);

      // Handle action buttons if present
      if (response.actionButton) {
        console.log('Action button available:', response.actionButton);
        // You can add UI for action buttons here
      }

    } catch (error) {
      console.error('Agent API error:', error);
      setError('Sorry, I encountered an error. Please try again.');
      
      // Add error message to chat
      const errorMessage = {
        id: Date.now() + 1,
        type: 'agent',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

    const startSimulation = async () => {
    if (isSimulating) return;

    if (!selectedProject) {
      setError('Please select a project first');
      return;
    }

    setIsSimulating(true);
    setError(null);

    try {
      // Call the backend simulation endpoint with the selected project ID and project type
      const result = await ApiClient.runSimulation(selectedProject.id, selectedProjectType);
      
      if (result.success) {
        // Clear existing messages
        setMessages([]);
        
        // Add welcome message
        const welcomeMessage = {
          id: Date.now(),
          type: 'agent',
          content: "Hi! I'm your AI Project Manager. I will create a roadmap for your project to help your idea come to life. To get started give me a description of your project.",
          timestamp: new Date()
        };
        setMessages([welcomeMessage]);
        
        // Process all conversation messages
        const conversationMessages = result.messages.map((msg, index) => ({
          id: Date.now() + index + 1,
          type: msg.role === 'user' ? 'user' : 'agent',
          content: msg.content,
          timestamp: new Date(msg.timestamp || Date.now())
        }));
        
        // Add conversation messages
        setMessages(prev => [...prev, ...conversationMessages]);
        
        // Update session and conversation state
        if (result.sessionId) {
          setSessionId(result.sessionId);
        }
        if (result.conversationState) {
          setConversationState(result.conversationState);
          if (result.conversationState.phase) {
            setCurrentPhase(result.conversationState.phase);
          }
        }
        
        // Refresh the selected project to get the updated roadmap data
        if (result.roadmap) {
          const updatedProject = {
            ...selectedProject,
            roadmap_data: result.roadmap,
            roadmapNodes: result.roadmap.nodes || [] // Ensure roadmapNodes is also updated
          };
          updateSelectedProject(updatedProject);
          console.log('✅ Updated selected project with new roadmap data');
          
          // Refresh the projects list to ensure all components have the latest data
          await refreshProjects();
        }
        
        console.log(`Simulation complete! Generated roadmap with ${result.totalRounds} conversation rounds.`);
      }
      
    } catch (error) {
      console.error('Simulation failed:', error);
      setError('Simulation failed. Please try again.');
    } finally {
      setIsSimulating(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Auto-resize textarea function
  const adjustTextareaHeight = () => {
    if (inputRef.current) {
      inputRef.current.style.height = 'auto';
      inputRef.current.style.height = `${inputRef.current.scrollHeight}px`;
    }
  };

  // Handle input change with auto-resize
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    // Small delay to ensure smooth resizing
    setTimeout(adjustTextareaHeight, 0);
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-4 w-12 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-md transition-all duration-300 flex items-center justify-center z-50 cursor-pointer"
        >
          <BiSolidFaceMask className="w-7 h-7" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-6 right-4 w-[450px] h-[450px] bg-white dark:bg-[#2a2a2a] rounded-2xl shadow-xl border border-gray-200 dark:border-[#3C3C3C] flex flex-col z-50">
          {/* Header */}
          <div className="flex items-center justify-between dark:text-white px-4 py-3 rounded-t-2xl">
            <div className="text-sm capitalize">
              {currentPhase.replace('_', ' ')} phase
            </div>
            <div className="flex items-center gap-2">
              {/* Project Type Dropdown */}
              <div className="relative" ref={projectTypeMenuRef}>
                {showProjectTypeMenu && (
                  <div className="absolute top-full right-0 mt-2 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-1 z-10">
                    {loadingProjectOptions ? (
                      <div className="px-3 py-2 text-sm text-gray-500 dark:text-gray-400">
                        Loading...
                      </div>
                    ) : (
                      availableProjectTypes.map((projectType) => (
                        <button
                          key={projectType.value}
                          onClick={() => handleProjectTypeSelect(projectType.value)}
                          className={`w-full text-left px-3 py-2 text-xs hover:bg-gray-100 dark:hover:bg-[#3A3A3A] transition-colors ${
                            selectedProjectType === projectType.value ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'
                          }`}
                        >
                          {projectType.label}
                        </button>
                      ))
                    )}
                  </div>
                )}
                
                <button
                  onClick={() => setShowProjectTypeMenu(!showProjectTypeMenu)}
                  disabled={isSimulating || loadingProjectOptions}
                  className={`p-1 rounded-lg text-xs font-medium transition-colors flex items-center gap-1 ${
                    isSimulating || loadingProjectOptions
                      ? 'text-gray-400 dark:text-gray-500 cursor-not-allowed'
                      : 'text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 cursor-pointer'
                  }`}
                  title="Select project type for simulation"
                >
                  <span className="text-xs">
                    {loadingProjectOptions ? 'Loading...' : availableProjectTypes.find(p => p.value === selectedProjectType)?.label || 'CodeMentor'}
                  </span>
                  <FaChevronDown className="w-3 h-3" />
                </button>
              </div>
              
              {/* Simulation Button */}
              <button
                onClick={startSimulation}
                disabled={isSimulating}
                className={`p-1 rounded-lg text-xs font-medium transition-colors ${
                  isSimulating 
                    ? 'dark:bg-gray-400 text-gray-200 cursor-not-allowed' 
                    : 'cursor-pointer'
                }`}
                title={`Simulate ${availableProjectTypes.find(p => p.value === selectedProjectType)?.label} conversation flow`}
              >
                <FaRobot className="w-5 h-5 text-gray-400 dark:text-gray-300 hover:text-gray-600 dark:hover:text-gray-100" />
              </button>
              
              {/* Close Button */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-500 cursor-pointer"
              >
                <RxCross2 className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`flex gap-2 max-w-[85%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                  {/* Message Bubble */}
                  <div className={`rounded-lg px-3 py-2 ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-[#3A3A3A] text-gray-800 dark:text-gray-200'
                  }`}>
                    <p className="text-sm">{message.content}</p>
                  </div>
                </div>
              </div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start">
                <div className="flex gap-2 max-w-[85%]">
                  <div className="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 rounded-full flex items-center justify-center flex-shrink-0">
                    <BiSolidFaceMask className="w-5 h-5 text-blue-500 dark:text-blue-400" />
                  </div>
                  <div className="bg-gray-100 dark:bg-[#3A3A3A] rounded-lg px-3 py-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="flex justify-start">
                <div className="flex gap-2 max-w-[85%]">
                  <div className="bg-red-100 dark:bg-red-900/30 rounded-lg px-3 py-2">
                    <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Simulation Status */}
            {isSimulating && (
              <div className="flex justify-start">
                <div className="flex gap-2 max-w-[85%]">
                  <div className="bg-blue-100 dark:bg-blue-900/30 rounded-lg px-3 py-2">
                    <div className="flex items-center gap-2">
                      <FaRobot className="w-4 h-4 text-blue-600 dark:text-blue-400 animate-pulse" />
                      <p className="text-sm text-blue-700 dark:text-blue-300">Simulating conversation...</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4">
            {/* Input Area with inline buttons */}
            <div className="bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] rounded-xl px-2 pb-2 pt-3 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 transition-all">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Ask me anything..."
                className="w-full resize-none bg-transparent text-sm focus:outline-none placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-gray-100 px-2 leading-5"
                rows="1"
                style={{ 
                  maxHeight: '120px', 
                  minHeight: '20px',
                  overflowY: 'auto'
                }}
              />
              
              {/* Button Container */}
              <div className="flex justify-between items-center pt-1">
                <div className="flex items-center gap-1 relative" ref={actionMenuRef}>
                  {/* Action Menu Dropdown */}
                  {showActionMenu && (
                    <div className="absolute bottom-full left-0 mb-2 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg shadow-lg py-1 min-w-[180px] z-10">
                      {actionOptions.map((option) => (
                        <button
                          key={option.id}
                          onClick={() => handleActionSelect(option.id)}
                          className={`w-full text-left px-3 py-2 text-sm hover:bg-gray-100 dark:hover:bg-[#3A3A3A] transition-colors ${
                            selectedAction === option.id ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'
                          }`}
                        >
                          <div className="font-medium">{option.label}</div>
                          <div className="text-xs text-gray-500 dark:text-gray-400">{option.description}</div>
                        </button>
                      ))}
                    </div>
                  )}

                  {/* Microphone Button */}
                  <button
                    className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer"
                    title="Voice input"
                  >
                    <FaMicrophone className="w-4.5 h-4.5" />
                  </button>
                  
                  {/* Action Selector Button */}
                  <button
                    onClick={() => setShowActionMenu(!showActionMenu)}
                    className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer flex items-center gap-1"
                    title={`Current action: ${actionOptions.find(opt => opt.id === selectedAction)?.label}`}
                  >
                    <span className="text-xs font-medium">{selectedAction}</span>
                    <FaChevronDown className='w-3 h-3' />
                  </button>
                </div>     
                
                {/* Send Button */}           
                <button
                    onClick={handleSendMessage}
                    disabled={!inputValue.trim() || isTyping}
                    className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] disabled:cursor-not-allowed cursor-pointer"
                    >
                    <FaCircleArrowUp className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Agent;
