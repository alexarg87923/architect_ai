import React, { useState, useRef, useEffect } from 'react';
import { FaCircleArrowUp, FaChevronDown } from "react-icons/fa6";
import { LuPaperclip } from "react-icons/lu";
import { MdAlternateEmail } from "react-icons/md";

const InputBox = ({ 
  inputValue, 
  setInputValue, 
  handleSendMessage, 
  isTyping,
  selectedAction,
  setSelectedAction,
  showActionMenu,
  setShowActionMenu,
  actionOptions,
  actionMenuRef,
  shouldFocus = false,
  disabled = false
}) => {
  const [showTooltip, setShowTooltip] = useState({ attachNodes: false, attachFiles: false, actionSelector: false });
  const [tooltipTimeouts, setTooltipTimeouts] = useState({ attachNodes: null, attachFiles: null, actionSelector: null });
  const inputRef = useRef(null);

  const handleActionSelect = (actionId) => {
    setSelectedAction(actionId);
    setShowActionMenu(false);
  };

  const handleTooltipEnter = (tooltipType) => {
    // Don't show tooltips when action menu is open
    if (showActionMenu) return;
    
    // Clear any existing timeout for this tooltip
    if (tooltipTimeouts[tooltipType]) {
      clearTimeout(tooltipTimeouts[tooltipType]);
    }
    
    // Set a new timeout to show the tooltip after 300ms
    const timeout = setTimeout(() => {
      setShowTooltip(prev => ({ ...prev, [tooltipType]: true }));
    }, 300);
    
    setTooltipTimeouts(prev => ({ ...prev, [tooltipType]: timeout }));
  };

  const handleTooltipLeave = (tooltipType) => {
    // Clear the timeout if it hasn't fired yet
    if (tooltipTimeouts[tooltipType]) {
      clearTimeout(tooltipTimeouts[tooltipType]);
      setTooltipTimeouts(prev => ({ ...prev, [tooltipType]: null }));
    }
    
    // Hide the tooltip immediately
    setShowTooltip(prev => ({ ...prev, [tooltipType]: false }));
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

  // Adjust textarea height when input value changes
  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  // Focus input when shouldFocus is true
  useEffect(() => {
    if (shouldFocus && inputRef.current) {
      inputRef.current.focus();
    }
  }, [shouldFocus]);

  // Cleanup tooltip timeouts on unmount
  useEffect(() => {
    return () => {
      Object.values(tooltipTimeouts).forEach(timeout => {
        if (timeout) clearTimeout(timeout);
      });
    };
  }, [tooltipTimeouts]);

  // Hide all tooltips when action menu opens
  useEffect(() => {
    if (showActionMenu) {
      // Clear all tooltip timeouts
      Object.values(tooltipTimeouts).forEach(timeout => {
        if (timeout) clearTimeout(timeout);
      });
      setTooltipTimeouts({ attachNodes: null, attachFiles: null, actionSelector: null });
      
      // Hide all visible tooltips
      setShowTooltip({ attachNodes: false, attachFiles: false, actionSelector: false });
    }
  }, [showActionMenu, tooltipTimeouts]);

  return (
    <div className="p-4">
      {/* Input Area with inline buttons */}
      <div className="bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] rounded-2xl px-2 pb-1.5 pt-2.5 focus-within:ring-2 focus-within:ring-blue-500 focus-within:border-blue-500 transition-all">
        {/* Attach Nodes Button (used to attach nodes as context when performing ) */}
        <div className="flex justify-start pb-2 pl-1">
          <div className="relative">
            <button
              className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer border border-gray-300 dark:border-[#3C3C3C]"
              onMouseEnter={() => handleTooltipEnter('attachNodes')}
              onMouseLeave={() => handleTooltipLeave('attachNodes')}
            >
              <MdAlternateEmail className="w-4 h-4" />
            </button>
            
            {/* Custom Tooltip for Attach Nodes */}
            {showTooltip.attachNodes && (
              <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1.5 bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] text-gray-900 dark:text-gray-100 text-xs px-2 py-1 rounded-md shadow-sm whitespace-nowrap z-20">
                Attach nodes as context
              </div>
            )}
          </div>
        </div>

        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything..."
          disabled={disabled}
          className="w-full resize-none bg-transparent text-sm focus:outline-none placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-gray-100 px-2 leading-5 disabled:opacity-50 disabled:cursor-not-allowed"
          rows="1"
          style={{ 
            maxHeight: '120px', 
            minHeight: '20px',
            overflowY: 'auto'
          }}
        />
        
        {/* Button Container */}
        <div className="flex justify-between items-center pt-0.5 pl-1">
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

            {/* Attach Files Button */}
            <div className="relative">
              <button
                className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer"
                onMouseEnter={() => handleTooltipEnter('attachFiles')}
                onMouseLeave={() => handleTooltipLeave('attachFiles')}
              >
                <LuPaperclip className="w-4 h-4" />
              </button>
              
              {/* Custom Tooltip for Attach Files */}
              {showTooltip.attachFiles && (
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1.5 bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] text-gray-900 dark:text-gray-100 text-xs px-2 py-1 rounded-md shadow-sm whitespace-nowrap z-20">
                  Attach files
                </div>
              )}
            </div>
            
            {/* Action Selector Button */}
            <div className="relative">
              <button
                onClick={() => setShowActionMenu(!showActionMenu)}
                className="p-1 text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 transition-colors rounded-lg hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer flex items-center gap-1"
                onMouseEnter={() => handleTooltipEnter('actionSelector')}
                onMouseLeave={() => handleTooltipLeave('actionSelector')}
              >
                <span className="text-xs font-medium">{selectedAction}</span>
                <FaChevronDown className='w-3 h-3' />
              </button>
              
              {/* Custom Tooltip for Action Selector */}
              {showTooltip.actionSelector && (
                <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-1.5 bg-gray-50 dark:bg-[#1a1a1a] border border-gray-300 dark:border-[#3C3C3C] text-gray-900 dark:text-gray-100 text-xs px-2 py-1 rounded-md shadow-sm whitespace-nowrap z-20">
                  Select action type
                </div>
              )}
            </div>
          </div>     
          
          {/* Send Button */}           
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isTyping || disabled}
            className={`p-1 text-gray-400 dark:text-gray-500 transition-colors rounded-lg disabled:cursor-not-allowed ${
                !(!inputValue.trim() || isTyping || disabled) 
                    ? 'hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-200 dark:hover:bg-[#3A3A3A] cursor-pointer' 
                    : 'cursor-not-allowed'
            }`}
          >
            <FaCircleArrowUp className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default InputBox;
