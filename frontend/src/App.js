import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Container } from '@mui/material';
import Home from './components/Home';
import Login from './components/Login';
import Pricing from './components/Pricing';
import Promotions from './components/Promotions';
import TradeSpend from './components/TradeSpend';
import CompetitorTracking from './components/CompetitorTracking';
import RevenueForecast from './components/RevenueForecast';

function App() {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/login">Login</Button>
          <Button color="inherit" component={Link} to="/pricing">Pricing</Button>
          <Button color="inherit" component={Link} to="/promotions">Promotions</Button>
          <Button color="inherit" component={Link} to="/trade-spend">Trade Spend</Button>
          <Button color="inherit" component={Link} to="/competitor-tracking">Competitor Tracking</Button>
          <Button color="inherit" component={Link} to="/revenue-forecast">Revenue Forecast</Button>
        </Toolbar>
      </AppBar>
      <Container>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/promotions" element={<Promotions />} />
          <Route path="/trade-spend" element={<TradeSpend />} />
          <Route path="/competitor-tracking" element={<CompetitorTracking />} />
          <Route path="/revenue-forecast" element={<RevenueForecast />} />
        </Routes>
      </Container>
    </>
  );
}

export default App;