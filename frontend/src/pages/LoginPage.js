import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { login } from "../api/endpoints";
import { TextField, Button, Box, Typography } from "@mui/material";

const LoginPage = () => {
  const { login: loginUser } = useContext(AuthContext);
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await login(credentials);
      loginUser(response.data);
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" mt={5}>
      <Typography variant="h4" gutterBottom>Login</Typography>
      <form onSubmit={handleSubmit}>
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
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Login
        </Button>
      </form>
    </Box>
  );
};

export default LoginPage;