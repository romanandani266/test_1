import React, { useState } from 'react';
import { TextField, Button, Typography } from '@mui/material';
import { login } from '../api';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleLogin = async () => {
    try {
      const data = await login(username, password);
      alert(`Login successful! Role: ${data.user_role}`);
    } catch (err) {
      setError(err.detail || 'Login failed');
    }
  };

  return (
    <div>
      <Typography variant="h4">Login</Typography>
      <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth />
      <Button variant="contained" onClick={handleLogin}>Login</Button>
      {error && <Typography color="error">{error}</Typography>}
    </div>
  );
};

export default Login;
