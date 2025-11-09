import { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { ProjectProvider } from './contexts/SelectedProjectContext.jsx';
import ProtectedRoute from './middleware/ProtectedRoute';
import Dashboard from './pages/Dashboard.jsx';
import Login from './pages/auth/Login.jsx';
import Admin from './pages/Admin.jsx';
import NotFound from './pages/NotFound.jsx';
import Landing from './pages/Landing.jsx';
import Waitlist from './pages/Waitlist.jsx';

/*
FUTURE IDEAS:
- Add github crawler which can be used to update the context of the Agent when the user has made changes to the project on github.
  - This will allow the Agent to understand the User's progress, and also judge the correctness of their approach (and update the Roadmap accordingly).

TODOS:
- DONE -- Connect Agent to the frontend Agent.jsx component (initial roadmap creation flow)
- DONE -- Add 2-3 more diverse LLM simulated project tests to the backend - test_roadmap_generation_only.py
- DONE -- Properly style the Agent.jsx component

- Improve the agent-user interaction for creating a project roadmap --> be like "It seems like you do not have a roadmap for this project. Let's create one together."

- Implement Backend flow for editing and expanding agent ACTIONS
- Implement regular chat with Agent (make sure that it has context of everything on the frontend and also previous chats with the User) (**IMPORTANT**)

- DONE -- Implement basic settings page (change password, change email, etc.)

- Create superuser in the db, and protect certain pages and endpoints from non-superusers (populate superuser in the seed_database.py script, this will be my account)
  - PROTECT: admin page, simulation endpoints (should not appear in the UI for non-superusers)

- Change the Landing page buttons if a logged in user is on the page
- Connect the waitlist form to the backend and to the Admin Panel
*/

function App() {
  const [isDark, setIsDark] = useState(() => {
    const savedTheme = localStorage.getItem("theme");
    return savedTheme === "dark";
  });

  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      root.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [isDark]);

  return (
    <AuthProvider>
      <ProjectProvider>
        <Router>
          <Routes>
            {/* Public Routes */}
            <Route path="/" element={<Landing isDark={isDark} toggleTheme={() => setIsDark(!isDark)} />} />
            <Route path="/login" element={<Login />} />
            <Route path="/waitlist" element={<Waitlist isDark={isDark} toggleTheme={() => setIsDark(!isDark)} />} />
            
            {/* Protected Routes */}
            <Route path="/dashboard" element={
              <ProtectedRoute>
                <Dashboard isDark={isDark} toggleTheme={() => setIsDark(!isDark)} />
              </ProtectedRoute>
            } />
            
            {/* Superuser Protected Routes */}
            <Route path="/admin" element={
              <ProtectedRoute requireSuperuser={true}>
                <Admin />
              </ProtectedRoute>
            } />

            {/* Redirects */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Router>
      </ProjectProvider>
    </AuthProvider>
  )
}

export default App
