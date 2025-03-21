import React, { useState, useEffect } from 'react';
import { fetchSales } from '../api';
import { Typography, List, ListItem } from '@mui/material';

const Sales = () => {
  const [sales, setSales] = useState([]);

  useEffect(() => {
    const loadSales = async () => {
      const data = await fetchSales();
      setSales(data);
    };
    loadSales();
  }, []);

  return (
    <div>
      <Typography variant="h4">Sales</Typography>
      <List>
        {sales.map((sale) => (
          <ListItem key={sale.sale_id}>
            Product ID: {sale.product_id}, Quantity Sold: {sale.quantity_sold}, Revenue: ${sale.total_revenue}
          </ListItem>
        ))}
      </List>
    </div>
  );
};

export default Sales;
