import React, { useState } from 'react';
import { TextField, Button } from '@mui/material';
import { login } from '../api';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
    try {
      const response = await login(username, password);
      alert(response.message);
    } catch (error) {
      alert('Login failed: ' + error.detail);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <TextField label="Username" value={username} onChange={(e) => setUsername(e.target.value)} fullWidth />
      <TextField label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} fullWidth />
      <Button variant="contained" color="primary" onClick={handleLogin}>Login</Button>
    </div>
  );
}

export default Login;