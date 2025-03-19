import React, { useEffect, useState } from "react";
import { api } from "../api";
import { Typography } from "@mui/material";

function SalesTrends() {
  const [salesTrends, setSalesTrends] = useState({});

  useEffect(() => {
    api.getSalesTrends()
      .then((response) => setSalesTrends(response.data))
      .catch((error) => console.error("Error fetching sales trends:", error));
  }, []);

  return (
    <div>
      <Typography variant="h4">Sales Trends</Typography>
      <pre>{JSON.stringify(salesTrends, null, 2)}</pre>
    </div>
  );
}

export default SalesTrends;
