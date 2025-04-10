import React, { useState, useEffect } from "react";
import { getAlerts } from "../api";
import { Typography, List, ListItem } from "@mui/material";

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const data = await getAlerts();
        setAlerts(data);
      } catch (err) {
        setError(err.detail || "Error fetching alerts");
      }
    };
    fetchAlerts();
  }, []);

  return (
    <div>
      <Typography variant="h4">Alerts</Typography>
      {error && <Typography color="error">{error}</Typography>}
      <List>
        {alerts.map((alert) => (
          <ListItem key={alert.alert_id}>
            {alert.product_id} - Threshold: {alert.threshold}
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Alerts;
