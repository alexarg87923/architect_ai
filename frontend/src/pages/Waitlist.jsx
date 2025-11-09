import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { HiOutlineMap, HiOutlineMoon, HiOutlineSun } from 'react-icons/hi';
import { 
  User,  
  Code, 
  Globe, 
  MessageSquare,
  ArrowLeft,
  CheckCircle
} from 'lucide-react';

const Waitlist = ({ isDark, toggleTheme }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    age: '',
    education: '',
    undergradYear: '',
    experienceLevel: '',
    primaryLanguage: '',
    heardFrom: '',
    projectTypes: [],
    motivation: '',
    additionalInfo: ''
  });

  const [isSubmitted, setIsSubmitted] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      setFormData(prev => ({
        ...prev,
        projectTypes: checked 
          ? [...prev.projectTypes, value]
          : prev.projectTypes.filter(type => type !== value)
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate that at least one project type is selected
    if (formData.projectTypes.length === 0) {
      alert('Please select at least one project type you are interested in building.');
      return;
    }
    
    setIsLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitted(true);
      setIsLoading(false);
    }, 1500);
  };

  if (isSubmitted) {
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
                to="/"
                className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
              >
                Back to Home
              </Link>
            </div>
          </div>
        </nav>

        {/* Success Message */}
        <div className="container mx-auto px-4 py-16">
          <div className="max-w-2xl mx-auto text-center">
            <div className="w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full flex items-center justify-center mx-auto mb-6">
              <CheckCircle className="w-8 h-8 text-green-600" />
            </div>
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              You're on the waitlist!
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
              Thanks for your interest in Roadmap AI! We'll notify you when we're ready to launch.
            </p>
            <Link
              to="/"
              className="inline-flex items-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Home</span>
            </Link>
          </div>
        </div>
      </div>
    );
  }

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
              to="/"
              className="text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </nav>

      {/* Form Section */}
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-3xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Join the Waitlist
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-300">
              Help us understand your needs and be among the first to try Roadmap AI
            </p>
          </div>

          <form onSubmit={handleSubmit} className="bg-white dark:bg-[#2a2a2a] rounded-xl shadow-lg p-8 border border-gray-200 dark:border-[#3C3C3C]">
            
            {/* Personal Information */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                <User className="w-5 h-5 mr-2" />
                Personal Information
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    First Name *
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Last Name *
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  />
                </div>
                
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Age Range
                  </label>
                  <select
                    name="age"
                    value={formData.age}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  >
                    <option value="">Select age range</option>
                    <option value="16-18">16-18</option>
                    <option value="19-22">19-22</option>
                    <option value="23-25">23-25</option>
                    <option value="26-30">26-30</option>
                    <option value="31-40">31-40</option>
                    <option value="40+">40+</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Current Occupation *
                  </label>
                  <select
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  >
                    <option value="">Select current occupation</option>
                    <option value="High School Student">High School Student</option>
                    <option value="Undergraduate Student">Undergraduate Student</option>
                    <option value="Graduate Student">Graduate Student</option>
                    <option value="Software Engineer">Software Engineer</option>
                    <option value="Frontend Developer">Frontend Developer</option>
                    <option value="Backend Developer">Backend Developer</option>
                    <option value="Full Stack Developer">Full Stack Developer</option>
                    <option value="Data Scientist">Data Scientist</option>
                    <option value="DevOps Engineer">DevOps Engineer</option>
                    <option value="Product Manager">Product Manager</option>
                    <option value="UX/UI Designer">UX/UI Designer</option>
                    <option value="QA Engineer">QA Engineer</option>
                    <option value="Student (Self-Taught)">Student (Self-Taught)</option>
                    <option value="Bootcamp Graduate">Bootcamp Graduate</option>
                    <option value="Career Changer">Career Changer</option>
                    <option value="Freelancer">Freelancer</option>
                    <option value="Unemployed">Unemployed</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
                
                {formData.education === 'Undergraduate Student' && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      What year are you in?
                    </label>
                    <select
                      name="undergradYear"
                      value={formData.undergradYear}
                      onChange={handleInputChange}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                    >
                      <option value="">Select year</option>
                      <option value="1st Year">1st Year</option>
                      <option value="2nd Year">2nd Year</option>
                      <option value="3rd Year">3rd Year</option>
                      <option value="4th Year">4th Year</option>
                      <option value="5th Year">5th Year +</option>
                    </select>
                  </div>
                )}
              </div>
            </div>

            {/* Technical Background */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                <Code className="w-5 h-5 mr-2" />
                Technical Background
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Programming Experience Level *
                  </label>
                  <select
                    name="experienceLevel"
                    value={formData.experienceLevel}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  >
                    <option value="">Select experience level</option>
                    <option value="Beginner">Beginner (0-1 years)</option>
                    <option value="Intermediate">Intermediate (1-3 years)</option>
                    <option value="Advanced">Advanced (3-5 years)</option>
                    <option value="Expert">Expert (5+ years)</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Primary Programming Language
                  </label>
                  <select
                    name="primaryLanguage"
                    value={formData.primaryLanguage}
                    onChange={handleInputChange}
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  >
                    <option value="">Select primary language</option>
                    <option value="JavaScript">JavaScript</option>
                    <option value="Python">Python</option>
                    <option value="Java">Java</option>
                    <option value="C++">C++</option>
                    <option value="C#">C#</option>
                    <option value="Go">Go</option>
                    <option value="Rust">Rust</option>
                    <option value="TypeScript">TypeScript</option>
                    <option value="PHP">PHP</option>
                    <option value="Ruby">Ruby</option>
                    <option value="Swift">Swift</option>
                    <option value="Kotlin">Kotlin</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Project Interest */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                <Globe className="w-5 h-5 mr-2" />
                Project Interest
              </h2>
              
              <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                  What types of projects are you interested in building? (Select all that apply) *
                </label>
                <div className="grid md:grid-cols-2 gap-3">
                  {[
                    'Web Applications',
                    'Mobile Apps',
                    'Data Science Projects',
                    'Machine Learning/AI',
                    'Game Development',
                    'Desktop Applications',
                    'API Development',
                    'E-commerce Platforms',
                    'Social Media Apps',
                    'Educational Tools',
                    'Productivity Apps',
                    'Portfolio Projects'
                  ].map((type) => (
                    <label key={type} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        name="projectTypes"
                        value={type}
                        checked={formData.projectTypes.includes(type)}
                        onChange={handleInputChange}
                        className="rounded border-gray-300 dark:border-gray-600 text-blue-600 focus:ring-blue-500"
                      />
                      <span className="text-sm text-gray-700 dark:text-gray-300">{type}</span>
                    </label>
                  ))}
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  What motivates you to build projects?
                </label>
                <textarea
                  name="motivation"
                  value={formData.motivation}
                  onChange={handleInputChange}
                  rows={3}
                  placeholder="e.g., Learning new technologies, building a portfolio, solving real-world problems..."
                  className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white resize-none"
                />
              </div>
            </div>

            {/* Timeline & Additional Info */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6 flex items-center">
                <MessageSquare className="w-5 h-5 mr-2" />
                Additional Information
              </h2>
              
              <div className="mb-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    How did you hear about Roadmap AI? *
                  </label>
                  <select
                    name="heardFrom"
                    value={formData.heardFrom}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white"
                  >
                    <option value="">Select source</option>
                    <option value="Social Media">Social Media</option>
                    <option value="GitHub">GitHub</option>
                    <option value="Friend/Colleague">Friend/Colleague</option>
                    <option value="Search Engine">Search Engine</option>
                    <option value="Blog/Article">Blog/Article</option>
                    <option value="YouTube">YouTube</option>
                    <option value="Reddit">Reddit</option>
                    <option value="Discord">Discord</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Any additional comments or questions?
                </label>
                <textarea
                  name="additionalInfo"
                  value={formData.additionalInfo}
                  onChange={handleInputChange}
                  rows={3}
                  placeholder="Tell us anything else you'd like us to know..."
                  className="w-full px-3 py-2 border border-gray-300 dark:border-[#3C3C3C] rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-[#1a1a1a] text-gray-900 dark:text-white resize-none"
                />
              </div>
            </div>

            {/* Submit Button */}
            <div className="text-center">
              <button
                type="submit"
                disabled={isLoading}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
              >
                {isLoading ? 'Submitting...' : 'Join Waitlist'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Waitlist;
