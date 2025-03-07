import React, { useEffect, useState } from "react";
import { api } from "../api";

const AuditLogs = () => {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await api.getAuditLogs(token);
        setLogs(response.data);
      } catch (error) {
        alert("Failed to fetch audit logs!");
      }
    };
    fetchLogs();
  }, []);

  return (
    <div>
      <h1>Audit Logs</h1>
      <pre>{JSON.stringify(logs, null, 2)}</pre>
    </div>
  );
};

export default AuditLogs;
