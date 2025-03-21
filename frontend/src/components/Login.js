import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";
import { login } from "../api";

const Login = () => {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const data = await login(credentials);
      localStorage.setItem("token", data.access_token);
      alert("Login successful!");
    } catch (err) {
      setError(err.detail || "Login failed");
    }
  };

  return (
    <div>
      <Typography variant="h4">Login</Typography>
      <TextField
        label="Username"
        value={credentials.username}
        onChange={(e) => setCredentials({ ...credentials, username: e.target.value })}
        fullWidth
        margin="normal"
      />
      <TextField
        label="Password"
        type="password"
        value={credentials.password}
        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        fullWidth
        margin="normal"
      />
      {error && <Typography color="error">{error}</Typography>}
      <Button variant="contained" color="primary" onClick={handleLogin}>
        Login
      </Button>
    </div>
  );
};

export default Login;
