import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Typography, List, ListItem } from "@mui/material";

function Notifications() {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    api.getNotifications()
      .then((response) => setNotifications(response.data))
      .catch((error) => console.error("Error fetching notifications:", error));
  }, []);

  return (
    <div>
      <Typography variant="h4">Notifications</Typography>
      <List>
        {notifications.map((notification, index) => (
          <ListItem key={index}>{notification.message}</ListItem>
        ))}
      </List>
    </div>
  );
}

export default Notifications;
