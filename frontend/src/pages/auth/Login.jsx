import React, { useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login, error, clearError } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    clearError();

    try {
      await login(email, password);
      navigate('/dashboard'); // Redirect to dashboard after successful login
    } catch (error) {
      console.error('Login failed:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const fillJohnDoeCredentials = () => {
    setEmail('johndoe@example.com');
    setPassword('dev123');
  };

  const fillBeckySmithCredentials = () => {
    setEmail('beckysmith@example.com');
    setPassword('dev123');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-[#1a1a1a] dark:to-[#2a2a2a]">
      <div className="max-w-md w-full space-y-8 p-8 bg-white dark:bg-[#2a2a2a] border border-gray-300 dark:border-[#3C3C3C] rounded-xl shadow-lg">
        <div className="text-center">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-2">
            Roadmap AI
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Sign in to your account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Email Address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="appearance-none relative block w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-gray-100 bg-white dark:bg-[#1a1a1a] rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="appearance-none relative block w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-gray-100 bg-white dark:bg-[#1a1a1a] rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Enter your password (optional for dev)"
            />
          </div>

          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}

          <div>
            <button
              type="submit"
              disabled={isLoading || !email}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Signing in...
                </span>
              ) : (
                'Sign in'
              )}
            </button>
          </div>

          {/* Development Credentials */}
          <div className="mt-6 p-4 bg-gray-50 dark:bg-[#1a1a1a] rounded-md border border-gray-200 dark:border-[#3C3C3C]">
            <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Development Credentials:</h3>
            <div className="grid grid-cols-2 gap-4">
              {/* John Doe */}
              <div className="space-y-2">
                <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                  <p><strong>John Doe</strong></p>
                  <p><strong>Email:</strong> johndoe@example.com</p>
                  <p><strong>Password:</strong> dev123 (optional)</p>
                </div>
                <button
                  type="button"
                  onClick={fillJohnDoeCredentials}
                  className="w-full text-xs text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 underline py-1 px-2 border border-indigo-200 dark:border-indigo-700 rounded hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors"
                >
                  Fill credentials automatically
                </button>
              </div>
              
              {/* Becky Smith */}
              <div className="space-y-2">
                <div className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                  <p><strong>Becky Smith</strong></p>
                  <p><strong>Email:</strong> beckysmith@example.com</p>
                  <p><strong>Password:</strong> dev123 (optional)</p>
                </div>
                <button
                  type="button"
                  onClick={fillBeckySmithCredentials}
                  className="w-full text-xs text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 underline py-1 px-2 border border-indigo-200 dark:border-indigo-700 rounded hover:bg-indigo-50 dark:hover:bg-indigo-900/20 transition-colors"
                >
                  Fill credentials automatically
                </button>
              </div>
            </div>
          </div>
        </form>

        <div className="text-center text-xs text-gray-500 dark:text-gray-400 mb-4">
          Development Mode - No signup required
        </div>
        
        <div className="text-center">
          <Link
            to="/"
            className="inline-flex items-center text-sm text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
