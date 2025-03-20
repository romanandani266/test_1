import React from "react";
import { Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import BlogDetailPage from "./pages/BlogDetailPage";
import CreateEditBlogPage from "./pages/CreateEditBlogPage";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/blogs/:id" element={<BlogDetailPage />} />
        <Route path="/create" element={<CreateEditBlogPage />} />
        <Route path="/edit/:id" element={<CreateEditBlogPage />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
