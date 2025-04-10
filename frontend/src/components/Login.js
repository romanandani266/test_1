import React, { useState } from "react";
import { login } from "../api";
import { Typography, TextField, Button } from "@mui/material";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const data = await login(username, password);
      setMessage(data.message);
      setError("");
    } catch (err) {
      setError(err.detail || "Login failed");
      setMessage("");
    }
  };

  return (
    <div>
      <Typography variant="h4">Login</Typography>
      <TextField
        label="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <TextField
        label="Password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <Button onClick={handleLogin}>Login</Button>
      {message && <Typography color="primary">{message}</Typography>}
      {error && <Typography color="error">{error}</Typography>}
    </div>
  );
};

export default Login;
