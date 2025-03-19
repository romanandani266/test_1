import React from "react";
import { Routes, Route, Link } from "react-router-dom";
import { AppBar, Toolbar, Button, Container } from "@mui/material";
import Inventory from "./components/Inventory";
import Notifications from "./components/Notifications";
import SalesTrends from "./components/SalesTrends";
import Login from "./components/Login";

function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">
            Inventory
          </Button>
          <Button color="inherit" component={Link} to="/notifications">
            Notifications
          </Button>
          <Button color="inherit" component={Link} to="/sales-trends">
            Sales Trends
          </Button>
          <Button color="inherit" component={Link} to="/login">
            Login
          </Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<Inventory />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/sales-trends" element={<SalesTrends />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </Container>
    </div>
  );
}

export default App;
