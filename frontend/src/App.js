import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import CreateEditBlog from './pages/CreateEditBlog';
import BlogDetailPage from './pages/BlogDetailPage';
import Header from './components/Header';

const App = () => {
  return (
    <div>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<CreateEditBlog />} />
        <Route path="/edit/:id" element={<CreateEditBlog />} />
        <Route path="/blog/:id" element={<BlogDetailPage />} />
      </Routes>
    </div>
  );
};

export default App;
