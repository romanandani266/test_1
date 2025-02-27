import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
import Dashboard from "../pages/Dashboard";
import InventoryPage from "../pages/InventoryPage";
import AlertsPage from "../pages/AlertsPage";
import SalesTrendsPage from "../pages/SalesTrendsPage";
import PrivateRoute from "./PrivateRoute";

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
        <Route path="/inventory" element={<PrivateRoute><InventoryPage /></PrivateRoute>} />
        <Route path="/alerts" element={<PrivateRoute><AlertsPage /></PrivateRoute>} />
        <Route path="/sales-trends" element={<PrivateRoute><SalesTrendsPage /></PrivateRoute>} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;