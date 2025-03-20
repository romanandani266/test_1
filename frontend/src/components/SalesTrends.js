import React, { useState } from "react";
import { fetchSalesTrends } from "../api";
import { TextField, Button, Typography } from "@mui/material";

const SalesTrends = () => {
  const [productId, setProductId] = useState("");
  const [timePeriod, setTimePeriod] = useState("");
  const [salesData, setSalesData] = useState(null);

  const handleFetchTrends = async () => {
    try {
      const data = await fetchSalesTrends(productId, timePeriod);
      setSalesData(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div>
      <Typography variant="h4">Sales Trends</Typography>
      <TextField label="Product ID" value={productId} onChange={(e) => setProductId(e.target.value)} fullWidth />
      <TextField label="Time Period" value={timePeriod} onChange={(e) => setTimePeriod(e.target.value)} fullWidth />
      <Button variant="contained" onClick={handleFetchTrends}>
        Fetch Trends
      </Button>
      {salesData && (
        <div>
          <Typography>Daily Sales: {salesData.daily_sales.join(", ")}</Typography>
          <Typography>Average Sales: {salesData.average_sales}</Typography>
          <Typography>Predicted Demand: {salesData.predicted_demand}</Typography>
        </div>
      )}
    </div>
  );
};

export default SalesTrends;
