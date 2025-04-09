import React, { useState } from "react";
import { api } from "../api";

const Integration = () => {
  const [integrationData, setIntegrationData] = useState({ system_id: "", data_format: "JSON", inventory_data: {} });
  const [message, setMessage] = useState("");

  const handleIntegration = async (e) => {
    e.preventDefault();
    try {
      const response = await api.pushIntegration(integrationData, "your-token-here");
      setMessage(response.message);
    } catch (err) {
      setMessage("Integration failed.");
    }
  };

  return (
    <div>
      <h2>Push Integration</h2>
      <form onSubmit={handleIntegration}>
        <input
          type="text"
          placeholder="System ID"
          value={integrationData.system_id}
          onChange={(e) => setIntegrationData({ ...integrationData, system_id: e.target.value })}
        />
        <select
          value={integrationData.data_format}
          onChange={(e) => setIntegrationData({ ...integrationData, data_format: e.target.value })}
        >
          <option value="JSON">JSON</option>
          <option value="XML">XML</option>
        </select>
        <textarea
          placeholder="Inventory Data"
          value={JSON.stringify(integrationData.inventory_data)}
          onChange={(e) => setIntegrationData({ ...integrationData, inventory_data: JSON.parse(e.target.value) })}
        />
        <button type="submit">Push Data</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Integration;
