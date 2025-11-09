import React, { useState, useRef, useEffect } from 'react';
import ApiClient from '../services/api';
import { useSelectedProject } from '../contexts/SelectedProjectContext';
import { useProjects } from '../hooks/useProjects';
import InputBox from './InputBox';
import WelcomeBubble from './WelcomeBubble';
// icon imports
import MascotSVG from '../assets/face-1.svg?react';
import { FaChevronDown } from "react-icons/fa6";
import { RxCross2 } from "react-icons/rx";


const Agent = () => {
  const { selectedProject, updateSelectedProject } = useSelectedProject();
  const { refreshProjects } = useProjects();
  const [isOpen, setIsOpen] = useState(() => {
    try {
      const savedState = localStorage.getItem('chatBoxOpen');
      return savedState ? JSON.parse(savedState) : false;
    } catch (error) {
      console.error('Failed to load chat box state:', error);
      return false;
    }
  });
  
  // Simple state that resets on page refresh
  const [showWelcomeBubble, setShowWelcomeBubble] = useState(true);
  
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
  const messagesEndRef = useRef(null);
  const actionMenuRef = useRef(null);

  // State for resizable height
  const [chatHeight, setChatHeight] = useState(() => {
    try {
      const savedHeight = localStorage.getItem('chatBoxHeight');
      return savedHeight ? parseInt(savedHeight, 10) : 450;
    } catch (error) {
      console.error('Failed to load chat box height:', error);
      return 450;
    }
  });
  const [isResizing, setIsResizing] = useState(false);
  const resizeStartRef = useRef({ startY: 0, startHeight: 0 });

  const actionOptions = [
    { id: 'Chat', label: 'Chat', description: 'General conversation' },
    { id: 'Edit', label: 'Edit', description: 'Edit specific node' },
    { id: 'Expand', label: 'Expand', description: 'Expand from node' },
    { id: 'Crawl', label: 'Crawl', description: 'Crawl specific resource' }
  ];

  // Auto-scroll to bottom when new messages are added
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Show welcome message when chat opens
  useEffect(() => {
    if (isOpen) {
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

  // Close action menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (actionMenuRef.current && !actionMenuRef.current.contains(event.target)) {
        setShowActionMenu(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Handle resize functionality
  const handleResizeStart = (e) => {
    e.preventDefault();
    setIsResizing(true);
    resizeStartRef.current = {
      startY: e.clientY,
      startHeight: chatHeight
    };
  };

  useEffect(() => {
    if (!isResizing) return;

    // Add cursor style to body
    document.body.style.cursor = 'ns-resize';
    document.body.style.userSelect = 'none';

    const handleMouseMove = (e) => {
      const deltaY = resizeStartRef.current.startY - e.clientY;
      const newHeight = Math.max(450, Math.min(800, resizeStartRef.current.startHeight + deltaY));
      setChatHeight(newHeight);
    };

    const handleMouseUp = () => {
      setIsResizing(false);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
      try {
        localStorage.setItem('chatBoxHeight', chatHeight.toString());
      } catch (error) {
        console.error('Failed to save chat box height:', error);
      }
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
      document.body.style.cursor = '';
      document.body.style.userSelect = '';
    };
  }, [isResizing, chatHeight]);

  // Function to handle chat box open/close
  const handleChatBoxToggle = (open) => {
    setIsOpen(open);
    if (open) {
      setShowWelcomeBubble(false); // Hide welcome bubble when chat opens
    }
    try {
      localStorage.setItem('chatBoxOpen', JSON.stringify(open));
    } catch (error) {
      console.error('Failed to save chat box state:', error);
    }
  };

  const handleWelcomeBubbleDismiss = () => {
    setShowWelcomeBubble(false);
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

    try {
      // Add project_id to conversation state if we have a selected project
      const stateWithProject = conversationState ? {
        ...conversationState,
        project_id: selectedProject?.id || null
      } : null;

      // Call the real agent API
      const response = await ApiClient.chatWithAgent(
        userMessage.content,
        sessionId,
        selectedAction.toLowerCase(),
        stateWithProject
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

        // If roadmap was generated, update the selected project with the roadmap data
        if (response.conversationState.current_roadmap && selectedProject) {
          const updatedProject = {
            ...selectedProject,
            roadmap_data: response.conversationState.current_roadmap,
            roadmapNodes: response.conversationState.current_roadmap.epics || []
          };
          updateSelectedProject(updatedProject);
          console.log('✅ Updated selected project with generated roadmap');

          // Refresh the projects list to ensure persistence
          refreshProjects();
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

  return (
    <>
      {/* Only show welcome bubble if chat is closed AND it hasn't been dismissed this session */}
      {!isOpen && showWelcomeBubble && (
        <WelcomeBubble 
          onDismiss={handleWelcomeBubbleDismiss}
        />
      )}

      {/* Regular Chat Button - always show when chat is closed */}
      {!isOpen && (
        <button
          onClick={() => handleChatBoxToggle(true)}
          className="fixed bottom-6 right-4 w-12 h-12 bg-blue-600 hover:scale-110 rounded-full shadow-md transition-all duration-150 ease-in-out flex items-center justify-center z-40 cursor-pointer"
        >
          <MascotSVG fill='#fff' className='w-8 h-8' />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div 
          className="fixed bottom-6 right-4 w-[450px] bg-white dark:bg-[#2a2a2a] rounded-2xl shadow-xl border border-gray-200 dark:border-[#3C3C3C] flex flex-col z-50"
          style={{ height: `${chatHeight}px` }}
        >
          {/* Resize Handle */}
          <div
            onMouseDown={handleResizeStart}
            className={`absolute top-0 left-0 right-0 h-2 cursor-ns-resize flex items-center justify-center group hover:bg-blue-500/10 rounded-t-2xl transition-colors ${
              isResizing ? 'bg-blue-500/20' : ''
            }`}
            style={{ zIndex: 10 }}
          >
            <div className={`w-12 h-1 rounded-full bg-gray-300 dark:bg-gray-600 group-hover:bg-blue-500 transition-colors ${
              isResizing ? 'bg-blue-500' : ''
            }`} />
          </div>

          {/* Header */}
          <div className="flex items-center justify-between dark:text-white px-4 py-3 rounded-t-2xl pt-4">
            <div className="text-sm font-medium flex items-center gap-1.5 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] rounded-xl py-1 px-2 cursor-pointer transition-colors">
              This chat <FaChevronDown className="w-3 h-3" />
            </div>
            <div className="flex items-center gap-2">
              {/* Close Button */}
              <button
                onClick={() => handleChatBoxToggle(false)}
                className="p-1 cursor-pointer hover:bg-gray-200 dark:hover:bg-[#3A3A3A] rounded-full transition-colors"
              >
                <RxCross2 className="w-5 h-5" />
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
                    <MascotSVG fill='#fff' className='w-8 h-8' />
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
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <InputBox
            inputValue={inputValue}
            setInputValue={setInputValue}
            handleSendMessage={handleSendMessage}
            isTyping={isTyping}
            selectedAction={selectedAction}
            setSelectedAction={setSelectedAction}
            showActionMenu={showActionMenu}
            setShowActionMenu={setShowActionMenu}
            actionOptions={actionOptions}
            actionMenuRef={actionMenuRef}
            shouldFocus={isOpen}
          />
        </div>
      )}
    </>
  );
};

export default Agent;