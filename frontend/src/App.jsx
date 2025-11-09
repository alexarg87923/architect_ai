import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Index from './pages/Index.jsx';
import NotFound from './pages/NotFound.jsx'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
