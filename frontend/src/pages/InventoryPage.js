import React, { useState, useEffect } from "react";
import { getInventory } from "../api/endpoints";
import { Box, Typography, CircularProgress } from "@mui/material";

const InventoryPage = () => {
  const [inventory, setInventory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const response = await getInventory();
        setInventory(response.data);
      } catch (err) {
        console.error("Failed to fetch inventory", err);
      } finally {
        setLoading(false);
      }
    };
    fetchInventory();
  }, []);

  if (loading) return <CircularProgress />;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Inventory</Typography>
      {inventory.map((item) => (
        <Box key={item.id} p={2} border="1px solid #ccc" mb={2}>
          <Typography>Product: {item.product_name}</Typography>
          <Typography>Quantity: {item.quantity}</Typography>
        </Box>
      ))}
    </Box>
  );
};

export default InventoryPage;