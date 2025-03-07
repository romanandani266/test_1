import React, { useState } from "react";
import api from "../../api";
import { handleApiError } from "../../utils";

const Login = () => {
  const [form, setForm] = useState({ username: "", password: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    api
      .post("/auth/login", form)
      .then((response) => {
        localStorage.setItem("token", response.data.access_token);
        alert("Login successful!");
      })
      .catch(handleApiError);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        value={form.username}
        onChange={(e) => setForm({ ...form, username: e.target.value })}
      />
      <input
        type="password"
        placeholder="Password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;