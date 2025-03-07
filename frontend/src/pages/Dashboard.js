import React from "react"; 
import { Link } from "react-router-dom";
import { Button, Box, Typography } from "@mui/material";
# test comment
const Dashboard = () => {
  return (
    <Box textAlign="center" mt={5}>
      <Typography variant="h4" gutterBottom>Welcome to the Dashboard</Typography>
      <Button component={Link} to="/inventory" variant="contained" color="primary" sx={{ m: 1 }}>
        Manage Inventory
      </Button>
      <Button component={Link} to="/alerts" variant="contained" color="secondary" sx={{ m: 1 }}>
        Manage Alerts
      </Button>
      <Button component={Link} to="/sales-trends" variant="contained" color="success" sx={{ m: 1 }}>
        View Sales Trends
      </Button>
    </Box>
  );
};

export default Dashboard;