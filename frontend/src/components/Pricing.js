import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';
import { optimizePricing } from '../api';

function Pricing() {
  const [productId, setProductId] = useState('');
  const [marketConditions, setMarketConditions] = useState('{}');

  const handleOptimize = async () => {
    try {
      const response = await optimizePricing({
        product_id: productId,
        market_conditions: JSON.parse(marketConditions),
        competitor_prices: {}
      });
      alert(`Optimized Price: ${response.optimized_price}`);
    } catch (error) {
      alert('Error optimizing pricing: ' + error.detail);
    }
  };

  return (
    <div>
      <h2>Pricing Optimization</h2>
      <TextField label="Product ID" value={productId} onChange={(e) => setProductId(e.target.value)} fullWidth />
      <TextField label="Market Conditions (JSON)" value={marketConditions} onChange={(e) => setMarketConditions(e.target.value)} fullWidth />
      <Button variant="contained" color="primary" onClick={handleOptimize}>Optimize</Button>
    </div>
  );
}

export default Pricing;