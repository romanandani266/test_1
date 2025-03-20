import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Container } from "@mui/material";
import Inventory from "./components/Inventory";
import RestockingAlerts from "./components/RestockingAlerts";
import SalesTrends from "./components/SalesTrends";
import ERPIntegration from "./components/ERPIntegration";
import Login from "./components/Login";

const App = () => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/inventory">Inventory</Button>
          <Button color="inherit" component={Link} to="/alerts">Restocking Alerts</Button>
          <Button color="inherit" component={Link} to="/sales-trends">Sales Trends</Button>
          <Button color="inherit" component={Link} to="/erp-integration">ERP Integration</Button>
          <Button color="inherit" component={Link} to="/login">Login</Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<h1>Welcome to Retail Inventory Management System</h1>} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/alerts" element={<RestockingAlerts />} />
          <Route path="/sales-trends" element={<SalesTrends />} />
          <Route path="/erp-integration" element={<ERPIntegration />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Container>
    </div>
  );
};

export default App;