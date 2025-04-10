import React, { useState, useEffect } from "react";
import { getInventory } from "../api";
import { Typography, List, ListItem } from "@mui/material";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const data = await getInventory();
        setInventory(data);
      } catch (err) {
        setError(err.detail || "Error fetching inventory");
      }
    };
    fetchInventory();
  }, []);

  return (
    <div>
      <Typography variant="h4">Inventory</Typography>
      {error && <Typography color="error">{error}</Typography>}
      <List>
        {inventory.map((item) => (
          <ListItem key={item.inventory_id}>
            {item.product_id} - {item.stock_level}
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Inventory;
