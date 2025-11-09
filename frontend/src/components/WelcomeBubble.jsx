import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const WelcomeBubble = ({ onDismiss }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [displayedText, setDisplayedText] = useState('');
    const [fullText, setFullText] = useState('');

    // Dynamic greeting messages based on time
    const greetingMessages = {
        morning: [
            "Good morning! Ready to start your day working on your project?",
            "Rise and shine! Time to make progress on your roadmap today."
        ],
        afternoon: [
            "Good afternoon! Perfect time to dive into your project work.",
            "Hey there! Ready to tackle some development tasks this afternoon?"
        ],
        evening: [
            "Good evening! Wind down by reviewing your project progress.",
            "Evening! How about some productive project work to end the day?"
        ],
        lateNight: [
            "Good night! Quick project check before bed?",
            "Hey night owl! Late-night coding session on your project?"
        ]
    };

    const firstTimeMessage = "I can help you create detailed roadmaps for your projects. Just describe your idea and I'll guide you through!";

    const getTimeBasedGreeting = () => {
        const hour = new Date().getHours();
        let timeCategory;
        
        if (hour >= 6 && hour < 12) {
            timeCategory = 'morning';
        } else if (hour >= 12 && hour < 18) {
            timeCategory = 'afternoon';
        } else if (hour >= 18 && hour < 23) {
            timeCategory = 'evening';
        } else {
            timeCategory = 'lateNight'; // 11pm - 5:59am
        }
        
        // Randomly select one of the variations for the time category
        const messages = greetingMessages[timeCategory];
        const randomIndex = Math.floor(Math.random() * messages.length);
        return messages[randomIndex];
    };

    const getMessage = () => {
        // Check if user has ever seen the welcome bubble before
        const hasSeenWelcome = localStorage.getItem('roadmap-ai-has-seen-welcome');
        
        if (!hasSeenWelcome) {
            // First time visitor - show the original message and mark as seen
            localStorage.setItem('roadmap-ai-has-seen-welcome', 'true');
            return firstTimeMessage;
        } else {
            // Returning visitor - show time-based greeting
            return getTimeBasedGreeting();
        }
    };

    useEffect(() => {
        // Set the message when component mounts
        setFullText(getMessage());
        
        // Always show after a short delay on page load
        const timer = setTimeout(() => {
            setIsVisible(true);
        }, 800);
        return () => clearTimeout(timer);
    }, []);

    useEffect(() => {
        if (isVisible && fullText) {
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
    }, [isVisible, fullText]);

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
                    className="fixed bottom-20.5 right-4 z-50"
                >
                    <div className="relative">
                        {/* Speech bubble with fixed width */}
                        <div className="bg-white dark:bg-[#2a2a2a] border-2 border-blue-200 dark:border-blue-500/30 rounded-xl p-4 shadow-lg w-[280px] relative">
                            {/* Close button */}
                            <button
                                onClick={handleDismiss}
                                className="absolute top-3 right-3 w-6 h-6 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-full flex items-center justify-center shadow-sm hover:bg-gray-50 dark:hover:bg-[#3A3A3A] transition-colors"
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
                            <div className="absolute -bottom-[6px] right-6 w-3 h-3 bg-white dark:bg-[#2a2a2a] border-b-2 border-r-2 border-blue-200 dark:border-blue-500/30 transform rotate-45"></div>
                        </div>
                    </div>
                </motion.div>
            )}
        </AnimatePresence>
    );
};

export default WelcomeBubble;