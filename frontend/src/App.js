import React from "react";
import { Routes, Route } from "react-router-dom";
import { CssBaseline, ThemeProvider } from "@mui/material";
import theme from "./theme";
import Navbar from "./components/Navbar";
import BlogList from "./components/BlogList";
import BlogDetail from "./components/BlogDetail";
import BlogForm from "./components/BlogForm";

const App = () => {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Navbar />
      <Routes>
        <Route path="/" element={<BlogList />} />
        <Route path="/blogs/:id" element={<BlogDetail />} />
        <Route path="/create" element={<BlogForm />} />
        <Route path="/edit/:id" element={<BlogForm />} />
      </Routes>
    </ThemeProvider>
  );
};

export default App;
