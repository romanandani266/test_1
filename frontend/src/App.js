import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { CssBaseline, ThemeProvider } from '@mui/material';
import theme from './theme';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import CreateEditBlog from './pages/CreateEditBlog';
import BlogDetailPage from './pages/BlogDetailPage';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<CreateEditBlog />} />
        <Route path="/edit/:id" element={<CreateEditBlog />} />
        <Route path="/blogs/:id" element={<BlogDetailPage />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;