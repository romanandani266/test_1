import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { CssBaseline, AppBar, Toolbar, Typography, Button } from "@mui/material";
import HomePage from "./pages/HomePage";
import CreateEditPage from "./pages/CreateEditPage";
import BlogDetailPage from "./pages/BlogDetailPage";

function App() {
  return (
    <>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            My Blog App
          </Typography>
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/create">
            Create Blog
          </Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/create" element={<CreateEditPage />} />
        <Route path="/edit/:id" element={<CreateEditPage />} />
        <Route path="/blogs/:id" element={<BlogDetailPage />} />
      </Routes>
    </>
  );
}

export default App;
