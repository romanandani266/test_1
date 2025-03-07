import React, { useEffect, useState } from "react";
import { getInventory } from "../api";
import { Container, Typography, List, ListItem } from "@mui/material";

function Inventory() {
  const [inventory, setInventory] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const token = localStorage.getItem("token");
        const data = await getInventory(token);
        setInventory(data);
      } catch (err) {
        setError(err.message);
      }
    };

    fetchInventory();
  }, []);

  return (
    <Container>
      <Typography variant="h4">Inventory</Typography>
      {error && <Typography color="error">{error}</Typography>}
      <List>
        {inventory.map((item) => (
          <ListItem key={item.id}>
            {item.name} - Quantity: {item.quantity} - Price: ${item.price}
          </ListItem>
        ))}
      </List>
    </Container>
  );
}

export default Inventory;
