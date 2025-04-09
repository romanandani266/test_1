import React, { useState, useEffect } from "react";
import { api } from "../api";

const Inventory = () => {
  const [inventory, setInventory] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInventory = async () => {
      try {
        const data = await api.getInventory();
        setInventory(data);
      } catch (err) {
        setError(err.message);
      }
    };
    fetchInventory();
  }, []);

  return (
    <div>
      <h2>Inventory</h2>
      {error && <p>Error: {error}</p>}
      <ul>
        {inventory.map((item) => (
          <li key={item.inventory_id}>
            {item.product_name} - {item.stock_level}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Inventory;
