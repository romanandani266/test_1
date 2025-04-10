import React, { useState } from "react";
import { getSalesTrends } from "../api";
import { Typography, Button, TextField } from "@mui/material";

const SalesTrends = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [trends, setTrends] = useState(null);
  const [error, setError] = useState("");

  const fetchTrends = async () => {
    try {
      const data = await getSalesTrends({ start_date: startDate, end_date: endDate });
      setTrends(data);
    } catch (err) {
      setError(err.detail || "Error fetching sales trends");
    }
  };

  return (
    <div>
      <Typography variant="h4">Sales Trends</Typography>
      <TextField
        label="Start Date"
        type="date"
        value={startDate}
        onChange={(e) => setStartDate(e.target.value)}
        InputLabelProps={{ shrink: true }}
      />
      <TextField
        label="End Date"
        type="date"
        value={endDate}
        onChange={(e) => setEndDate(e.target.value)}
        InputLabelProps={{ shrink: true }}
      />
      <Button onClick={fetchTrends}>Fetch Trends</Button>
      {error && <Typography color="error">{error}</Typography>}
      {trends && (
        <div>
          <Typography>Total Sales: {trends.total_sales}</Typography>
          <Typography>Average Sales: {trends.average_sales}</Typography>
          <Typography>Peak Sales Period: {trends.peak_sales_period}</Typography>
        </div>
      )}
    </div>
  );
};

export default SalesTrends;
