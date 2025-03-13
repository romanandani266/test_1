import React from "react";
import { Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import CreateEditPage from "./pages/CreateEditPage";
import BlogDetailPage from "./pages/BlogDetailPage";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create" element={<CreateEditPage />} />
        <Route path="/edit/:id" element={<CreateEditPage />} />
        <Route path="/blogs/:id" element={<BlogDetailPage />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
