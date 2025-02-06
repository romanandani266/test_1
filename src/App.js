import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import Dashboard from './components/Dashboard/Dashboard';
import InventoryList from './components/Inventory/InventoryList';
import SalesReport from './components/Sales/SalesReport';

const App = () => {
  return (
    <Router>
      <Switch>
        <Route path="/login" component={Login} />
        <Route path="/register" component={Register} />
        <Route path="/dashboard" component={Dashboard} />
        <Route path="/inventory" component={InventoryList} />
        <Route path="/sales" component={SalesReport} />
      </Switch>
    </Router>
  );
};

export default App;