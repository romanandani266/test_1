import React, { useState, useEffect } from 'react';
import { fetchNotifications } from '../api';
import { Typography, List, ListItem } from '@mui/material';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const loadNotifications = async () => {
      const data = await fetchNotifications();
      setNotifications(data);
    };
    loadNotifications();
  }, []);

  return (
    <div>
      <Typography variant="h4">Notifications</Typography>
      <List>
        {notifications.map((notification) => (
          <ListItem key={notification.notification_id}>
            {notification.message}
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Notifications;
