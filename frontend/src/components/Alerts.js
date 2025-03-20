import React, { useEffect, useState } from "react";
import { fetchAlerts, acknowledgeAlert } from "../api";
import { Typography, List, ListItem, Button } from "@mui/material";

const Alerts = () => {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const loadAlerts = async () => {
      try {
        const data = await fetchAlerts();
        setAlerts(data);
      } catch (err) {
        console.error(err);
      }
    };
    loadAlerts();
  }, []);

  const handleAcknowledge = async (alertId) => {
    try {
      await acknowledgeAlert(alertId);
      setAlerts(alerts.filter((alert) => alert.alert_id !== alertId));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <Typography variant="h4">Alerts</Typography>
      <List>
        {alerts.map((alert) => (
          <ListItem key={alert.alert_id}>
            <Typography>{`${alert.product_name} - Current Stock: ${alert.current_stock}, Threshold: ${alert.threshold}`}</Typography>
            <Button onClick={() => handleAcknowledge(alert.alert_id)}>Acknowledge</Button>
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Alerts;
