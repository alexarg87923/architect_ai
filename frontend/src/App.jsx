import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ProjectProvider } from './contexts/ProjectContext';
import Index from './pages/Index.jsx';
import NotFound from './pages/NotFound.jsx'

function App() {

  return (
    <ProjectProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Index />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </ProjectProvider>
  )
}

export default App
