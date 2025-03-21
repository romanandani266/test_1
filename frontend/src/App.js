import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Container } from '@mui/material';
import Login from './components/Login';
import Inventory from './components/Inventory';
import Notifications from './components/Notifications';
import Sales from './components/Sales';

const App = () => {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/inventory">Inventory</Button>
          <Button color="inherit" component={Link} to="/notifications">Notifications</Button>
          <Button color="inherit" component={Link} to="/sales">Sales</Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/notifications" element={<Notifications />} />
          <Route path="/sales" element={<Sales />} />
        </Routes>
      </Container>
    </div>
  );
};

export default App;
