import React, { useState, useEffect } from 'react';
import { fetchInventory, addInventory } from '../api';
import { Typography, Button, TextField, List, ListItem } from '@mui/material';

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [newItem, setNewItem] = useState({ product_id: '', product_name: '', stock_level: 0, threshold: 0 });

  useEffect(() => {
    const loadInventory = async () => {
      const data = await fetchInventory();
      setInventory(data);
    };
    loadInventory();
  }, []);

  const handleAddItem = async () => {
    await addInventory(newItem);
    setInventory([...inventory, newItem]);
  };

  return (
    <div>
      <Typography variant="h4">Inventory</Typography>
      <List>
        {inventory.map((item) => (
          <ListItem key={item.product_id}>
            {item.product_name} - Stock: {item.stock_level} - Threshold: {item.threshold}
          </ListItem>
        ))}
      </List>
      <TextField label="Product ID" onChange={(e) => setNewItem({ ...newItem, product_id: e.target.value })} />
      <TextField label="Product Name" onChange={(e) => setNewItem({ ...newItem, product_name: e.target.value })} />
      <TextField label="Stock Level" type="number" onChange={(e) => setNewItem({ ...newItem, stock_level: parseInt(e.target.value) })} />
      <TextField label="Threshold" type="number" onChange={(e) => setNewItem({ ...newItem, threshold: parseInt(e.target.value) })} />
      <Button variant="contained" onClick={handleAddItem}>Add Item</Button>
    </div>
  );
};

export default Inventory;
