import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from '../pages/LoginPage';
import Dashboard from '../pages/Dashboard';
import InventoryPage from '../pages/InventoryPage';
import AlertsPage from '../pages/AlertsPage';
import SalesPage from '../pages/SalesPage';

const AppRoutes = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/inventory" element={<InventoryPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/sales" element={<SalesPage />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;