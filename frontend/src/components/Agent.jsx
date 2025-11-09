import React, { useState, useRef, useEffect } from 'react';
import { FaCircleArrowUp, FaMicrophone, FaChevronDown } from "react-icons/fa6";
import { RxCross2 } from "react-icons/rx";
import { BiSolidFaceMask } from "react-icons/bi";

const Agent = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [showActionMenu, setShowActionMenu] = useState(false);
  const [selectedAction, setSelectedAction] = useState('Chat');
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'agent',
      content: "Hi! I'm your AI Product Manager. I'm here to help you develop a roadmap and keep you accountable. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);
  const actionMenuRef = useRef(null);

  const actionOptions = [
    { id: 'Chat', label: 'Chat', description: 'General conversation' },
    { id: 'Edit', label: 'Edit', description: 'Edit specific node' },
    { id: 'Expand', label: 'Expand', description: 'Expand from node' }
  ];

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
    }
  }, [isOpen]);

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

  const handleActionSelect = (actionId) => {
    setSelectedAction(actionId);
    setShowActionMenu(false);
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

    // Simulate AI response (replace with actual API call)
    setTimeout(() => {
      const agentResponse = {
        id: Date.now() + 1,
        type: 'agent',
        content: generateAgentResponse(userMessage.content),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, agentResponse]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds
  };

  const generateAgentResponse = (userInput) => {
    // Simple response logic (replace with actual AI integration)
    const input = userInput.toLowerCase();
    
    if (input.includes('roadmap') || input.includes('plan')) {
      return "Great! Let's work on your roadmap. What's the main goal or product you're working on? I can help you break it down into phases and set realistic milestones.";
    } else if (input.includes('goal') || input.includes('objective')) {
      return "Setting clear goals is crucial! I recommend using the SMART framework: Specific, Measurable, Achievable, Relevant, and Time-bound. What's your primary objective?";
    } else if (input.includes('help') || input.includes('stuck')) {
      return "I'm here to help! Whether you need assistance with prioritization, timeline planning, or breaking down complex tasks, just let me know what's challenging you.";
    } else if (input.includes('hello') || input.includes('hi')) {
      return "Hello! I'm excited to help you build an amazing roadmap. What project or initiative are you working on?";
    } else {
      return "That's interesting! As your product manager, I'd love to help you turn that into actionable steps. Can you tell me more about your current priorities and timeline?";
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <>
      {/* Chat Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-8 right-8 w-12 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-md transition-all duration-300 flex items-center justify-center z-50 cursor-pointer"
        >
          <BiSolidFaceMask className="w-7 h-7" />
        </button>
      )}

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-8 right-8 w-[450px] h-[450px] bg-white dark:bg-[#2a2a2a] rounded-2xl shadow-xl border border-gray-200 dark:border-[#3C3C3C] flex flex-col z-50">
          {/* Header */}
          <div className="flex items-center justify-between p-4 bg-blue-600 dark:bg-blue-700 text-white rounded-t-2xl">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 bg-blue-500 dark:bg-blue-600 rounded-full flex items-center justify-center">
                
                <BiSolidFaceMask className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-semibold">Product Manager</h3>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1 rounded-full bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-500 cursor-pointer"
            >
              <RxCross2 className="w-4 h-4" />
            </button>
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
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-4">
            {/* Input Area with inline buttons */}
            <div className="bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] rounded-xl px-2 pb-2 pt-3 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 transition-all">
              <textarea
                ref={inputRef}
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me anything..."
                className="w-full resize-none bg-transparent text-sm focus:outline-none placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-gray-100 px-2"
                rows="1"
                style={{ maxHeight: '100px', minHeight: '20px' }}
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
