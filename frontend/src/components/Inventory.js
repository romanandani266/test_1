import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Typography, List, ListItem } from "@mui/material";

function Inventory() {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    api.getInventory()
      .then((response) => setInventory(response.data))
      .catch((error) => console.error("Error fetching inventory:", error));
  }, []);

  return (
    <div>
      <Typography variant="h4">Inventory</Typography>
      <List>
        {inventory.map((item) => (
          <ListItem key={item.product_id}>
            {item.product_name} - {item.stock_level}
          </ListItem>
        ))}
      </List>
    </div>
  );
}

export default Inventory;
