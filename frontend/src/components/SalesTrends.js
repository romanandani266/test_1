import React, { useState } from "react";
import { api } from "../api";

const SalesTrends = () => {
  const [trends, setTrends] = useState([]);
  const [filters, setFilters] = useState({ start_date: "", end_date: "" });

  const fetchTrends = async () => {
    try {
      const data = await api.getSalesTrends(filters);
      setTrends(data.trends);
    } catch (err) {
      console.error("Error fetching sales trends:", err);
    }
  };

  return (
    <div>
      <h2>Sales Trends</h2>
      <input
        type="date"
        value={filters.start_date}
        onChange={(e) => setFilters({ ...filters, start_date: e.target.value })}
      />
      <input
        type="date"
        value={filters.end_date}
        onChange={(e) => setFilters({ ...filters, end_date: e.target.value })}
      />
      <button onClick={fetchTrends}>Fetch Trends</button>
      <ul>
        {trends.map((trend, index) => (
          <li key={index}>
            {trend.date}: {trend.sales}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SalesTrends;
