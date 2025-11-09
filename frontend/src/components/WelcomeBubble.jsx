import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const WelcomeBubble = ({ onDismiss, onOpenChat }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [displayedText, setDisplayedText] = useState('');
    const fullText = "I can help you create detailed roadmaps for your projects. Just describe your idea and I'll guide you through!";

    useEffect(() => {
        // Always show after a short delay on page load
        const timer = setTimeout(() => {
            setIsVisible(true);
        }, 800);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        if (isVisible) {
            let index = 0;
            const typingInterval = setInterval(() => {
                if (index <= fullText.length) {
                    setDisplayedText(fullText.slice(0, index));
                    index++;
                } else {
                    clearInterval(typingInterval);
                }
            }, 15); // Adjust speed here (lower = faster)

            return () => clearInterval(typingInterval);
        }
    }, [isVisible]);

    const handleDismiss = () => {
        setIsVisible(false);
        if (onDismiss) onDismiss();
    };



    return (
        <AnimatePresence>
            {isVisible && (
                <motion.div
                    initial={{ opacity: 0, scale: 0.8, y: 20 }}
                    animate={{
                        opacity: 1,
                        scale: 1,
                        y: 0,
                    }}
                    exit={{
                        opacity: 0,
                        scale: 0.8,
                        y: 20,
                        transition: { duration: 0.2 }
                    }}
                    transition={{
                        type: "spring",
                        stiffness: 260,
                        damping: 20,
                        duration: 0.6
                    }}
                    className="fixed bottom-20 right-4 z-50"
                >
                    <div className="relative">
                        {/* Speech bubble with fixed width */}
                        <div className="bg-white dark:bg-[#2a2a2a] border-2 border-blue-200 dark:border-blue-500/30 rounded-xl p-4 shadow-lg w-[280px] relative">
                            {/* Close button */}
                            <button
                                onClick={handleDismiss}
                                className="absolute -top-2 -right-2 w-6 h-6 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-full flex items-center justify-center shadow-sm hover:bg-gray-50 dark:hover:bg-[#3A3A3A] transition-colors"
                            >
                                <span className="text-gray-400 dark:text-gray-500 text-xs">✕</span>
                            </button>

                            {/* Message content */}
                            <div className="space-y-3">
                                <div className="flex items-center gap-2">
                            
                                    <span className="font-semibold text-gray-900 dark:text-white text-sm">
                                        Hey there! I'm your AI PM
                                    </span>
                                </div>
                                <div className="h-[100px]">
                                    <p className="text-sm text-gray-600 dark:text-gray-300 leading-relaxed">
                                        {displayedText}
                                    </p>
                                </div>
                            </div>

                            {/* Speech bubble tail */}
                            <div className="absolute -bottom-[6px] right-8 w-3 h-3 bg-white dark:bg-[#2a2a2a] border-b border-r border-gray-200 dark:border-[#3C3C3C] transform rotate-45"></div>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default WelcomeBubble;