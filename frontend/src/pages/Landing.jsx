import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Brain, 
  Rocket, 
  CheckCircle, 
  ArrowRight,
  Code,
  BarChart3,
  MessageSquare
} from 'lucide-react';
import { HiOutlineMap, HiOutlineMoon, HiOutlineSun } from 'react-icons/hi';

const Landing = ({ isDark, toggleTheme }) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-[#1a1a1a]">
      {/* Navigation */}
      <nav className="container mx-auto px-4 py-6">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <HiOutlineMap className="w-8 h-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-900 dark:text-white">Roadmap AI</span>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-[#3A3A3A] transition-colors"
            >
              {isDark ? (
                <HiOutlineSun className="w-6 h-6 text-gray-700 dark:text-gray-300" />
              ) : (
                <HiOutlineMoon className="w-6 h-6 text-gray-700 dark:text-gray-300" />
              )}
            </button>
            <Link
              to="/login"
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Login
            </Link>
            <Link
              to="/waitlist"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Join Waitlist
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            AI-Powered Project
            <span className="text-blue-600 dark:text-blue-400"> Roadmaps</span>
          </h1>
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Transform your ideas into actionable roadmaps with intelligent AI assistance. 
            Built for students and developers building personal projects.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/waitlist"
              className="border-2 border-blue-600 text-blue-600 dark:text-blue-400 px-8 py-4 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors text-lg font-semibold"
            >
              Join Waitlist
            </Link>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Why Choose Roadmap AI?
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Our AI understands your project goals and creates detailed, actionable roadmaps 
            that guide you from concept to completion.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center mb-6">
              <Brain className="w-6 h-6 text-blue-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              AI Roadmap Generation
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Get detailed, step-by-step roadmaps tailored to your project goals, 
              tech stack, and timeline requirements.
            </p>
          </div>

          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-green-100 dark:bg-green-900/30 rounded-lg flex items-center justify-center mb-6">
              <Code className="w-6 h-6 text-green-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Smart Task Management
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Organize your daily todos and ideas with intelligent categorization 
              and progress tracking.
            </p>
          </div>

          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-purple-100 dark:bg-purple-900/30 rounded-lg flex items-center justify-center mb-6">
              <MessageSquare className="w-6 h-6 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              AI Project Assistant
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Chat with your AI assistant for guidance, code reviews, and 
              project-specific advice throughout development.
            </p>
          </div>

          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-orange-100 dark:bg-orange-900/30 rounded-lg flex items-center justify-center mb-6">
              <BarChart3 className="w-6 h-6 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Visual Progress Tracking
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              See your project progress with beautiful visual roadmaps and 
              milestone tracking.
            </p>
          </div>

          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-red-100 dark:bg-red-900/30 rounded-lg flex items-center justify-center mb-6">
              <Rocket className="w-6 h-6 text-red-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Student-Focused
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Designed specifically for students and developers working on 
              personal projects and portfolio pieces.
            </p>
          </div>

          <div className="bg-white dark:bg-[#2a2a2a] p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow border border-gray-200 dark:border-[#3C3C3C]">
            <div className="w-12 h-12 bg-indigo-100 dark:bg-indigo-900/30 rounded-lg flex items-center justify-center mb-6">
              <CheckCircle className="w-6 h-6 text-indigo-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Accountability & Motivation
            </h3>
            <p className="text-gray-600 dark:text-gray-300">
              Stay motivated with progress tracking, AI encouragement, and 
              clear milestone achievements.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="bg-white dark:bg-[#2a2a2a] rounded-2xl p-12 text-center border border-gray-200 dark:border-[#3C3C3C] shadow-lg">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Ready to Build Your Next Project?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8 max-w-2xl mx-auto">
            Join the waitlist to be among the first students and developers 
            using Roadmap AI to bring their ideas to life.
          </p>
          <Link
            to="/waitlist"
            className="bg-blue-600 text-white px-8 py-4 rounded-lg hover:bg-blue-700 transition-colors text-lg font-semibold inline-flex items-center space-x-2"
          >
            <span>Join Waitlist</span>
            <ArrowRight className="w-5 h-5" />
          </Link>
        </div>
      </div>

      {/* Footer */}
      <footer className="container mx-auto px-4 py-8 border-t border-gray-200 dark:border-[#3C3C3C]">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="flex items-center space-x-2 mb-4 md:mb-0">
            <HiOutlineMap className="w-6 h-6 text-blue-600" />
            <span className="text-lg font-semibold text-gray-900 dark:text-white">Roadmap AI</span>
          </div>
          
          {/* Center section */}
          <div className="flex items-center space-x-4 mb-4 md:mb-0">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Made by{' '}
              <a 
                href="https://github.com/hpitta26" 
                target="_blank" 
                rel="noopener noreferrer"
                className="underline"
              >
                Henrique
              </a>
            </span>
            <a 
              href="https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-sm text-blue-600 dark:text-blue-400"
            >
              Join our Discord!
            </a>
          </div>
          
          <div className="ml-5 text-sm text-gray-600 dark:text-gray-400">
            <span>Roadmap AI v0.1</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing; 