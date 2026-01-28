import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Dashboard from './pages/Dashboard';
import FAQ from './pages/FAQ';
import News from './pages/News';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Landing />} />
        <Route path='/dashboard' element={<Dashboard />} />
        <Route path='/faq' element={<FAQ />} />
        <Route path='/news' element={<News />} />
      </Routes>
    </BrowserRouter>
  );
}