import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { Container, AppBar, Toolbar, Button } from "@mui/material";
import Inventory from "./components/Inventory";
import Alerts from "./components/Alerts";
import SalesTrends from "./components/SalesTrends";
import Login from "./components/Login";
import Integration from "./components/Integration";

const App = () => {
  return (
    <Container>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/inventory">
            Inventory
          </Button>
          <Button color="inherit" component={Link} to="/alerts">
            Alerts
          </Button>
          <Button color="inherit" component={Link} to="/sales-trends">
            Sales Trends
          </Button>
          <Button color="inherit" component={Link} to="/integration">
            Integration
          </Button>
          <Button color="inherit" component={Link} to="/login">
            Login
          </Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/" element={<h1>Welcome to Retail Inventory Management</h1>} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/sales-trends" element={<SalesTrends />} />
        <Route path="/integration" element={<Integration />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Container>
  );
};

export default App;
