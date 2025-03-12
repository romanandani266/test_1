import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { Container, AppBar, Toolbar, Button } from '@mui/material';
import Home from './components/Home';
import Products from './components/Products';
import Alerts from './components/Alerts';
import Login from './components/Login';
import SalesTrend from './components/SalesTrend';

const App = () => {
  return (
    <Container>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/products">Products</Button>
          <Button color="inherit" component={Link} to="/alerts">Alerts</Button>
          <Button color="inherit" component={Link} to="/login">Login</Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/products" element={<Products />} />
        <Route path="/alerts" element={<Alerts />} />
        <Route path="/login" element={<Login />} />
        <Route path="/sales-trend/:id" element={<SalesTrend />} />
      </Routes>
    </Container>
  );
};

export default App;
