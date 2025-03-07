import React from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Inventory from "./components/Inventory";
import UserRights from "./components/UserRights";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/user-rights" element={<UserRights />} />
      </Routes>
    </div>
  );
}

export default App;
