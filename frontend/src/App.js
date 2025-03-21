import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Container } from "@mui/material";
import Inventory from "./components/Inventory";
import Login from "./components/Login";
import RestockingAlerts from "./components/RestockingAlerts";
import SalesTrends from "./components/SalesTrends";
import Notifications from "./components/Notifications";

const App = () => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">
            Home
          </Button>
          <Button color="inherit" component={Link} to="/inventory">
            Inventory
          </Button>
          <Button color="inherit" component={Link} to="/alerts">
            Restocking Alerts
          </Button>
          <Button color="inherit" component={Link} to="/sales-trends">
            Sales Trends
          </Button>
          <Button color="inherit" component={Link} to="/notifications">
            Notifications
          </Button>
        </Toolbar>
      </AppBar>

      <Container>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/alerts" element={<RestockingAlerts />} />
          <Route path="/sales-trends" element={<SalesTrends />} />
          <Route path="/notifications" element={<Notifications />} />
        </Routes>
      </Container>
    </div>
  );
};

export default App;
