import React, { useState } from "react";
import { login } from "../api";
import { TextField, Button, Typography } from "@mui/material";

const Login = () => {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [loginResponse, setLoginResponse] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await login(credentials);
      setLoginResponse(response);
    } catch (error) {
      console.error("Error logging in:", error);
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
      />
      <TextField
        label="Password"
        type="password"
        value={credentials.password}
        onChange={(e) => setCredentials({ ...credentials, password: e.target.value })}
        fullWidth
      />
      <Button variant="contained" onClick={handleSubmit}>Submit</Button>
      {loginResponse && <Typography>{`Access Token: ${loginResponse.access_token}`}</Typography>}
    </div>
  );
};

export default Login;