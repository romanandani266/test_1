import React, { useState } from "react";
import { api } from "../api";

const Alerts = () => {
  const [alertData, setAlertData] = useState({ product_id: "", threshold: 0 });
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.createAlert(alertData, "your-token-here");
      setMessage(response.message);
    } catch (err) {
      setMessage("Error creating alert.");
    }
  };

  return (
    <div>
      <h2>Create Alert</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Product ID"
          value={alertData.product_id}
          onChange={(e) => setAlertData({ ...alertData, product_id: e.target.value })}
        />
        <input
          type="number"
          placeholder="Threshold"
          value={alertData.threshold}
          onChange={(e) => setAlertData({ ...alertData, threshold: e.target.value })}
        />
        <button type="submit">Create Alert</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Alerts;
