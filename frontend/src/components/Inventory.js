import React, { useEffect, useState } from "react";
import { fetchInventory } from "../api";
import { Typography, List, ListItem, ListItemText } from "@mui/material";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const loadInventory = async () => {
      try {
        const data = await fetchInventory();
        setInventory(data);
      } catch (err) {
        console.error(err);
      }
    };
    loadInventory();
  }, []);

  return (
    <div>
      <Typography variant="h4">Inventory</Typography>
      <List>
        {inventory.map((item) => (
          <ListItem key={item.product_id}>
            <ListItemText primary={`${item.product_name} - Stock: ${item.stock_level}`} />
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Inventory;
