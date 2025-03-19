import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import BlogEditor from "./pages/BlogEditor";
import BlogDetails from "./components/BlogDetails";

const App = () => {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/create" element={<BlogEditor />} />
        <Route path="/blogs/:id" element={<BlogDetails />} />
      </Routes>
    </div>
  );
};

export default App;
