import React, { useState } from "react";
import { api } from "../api";

const Register = () => {
  const [form, setForm] = useState({ username: "", role: "", password: "" });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.register(form);
      alert("Registration successful!");
    } catch (error) {
      alert("Registration failed!");
    }
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
        type="text"
        placeholder="Role"
        value={form.role}
        onChange={(e) => setForm({ ...form, role: e.target.value })}
      />
      <input
        type="password"
        placeholder="Password"
        value={form.password}
        onChange={(e) => setForm({ ...form, password: e.target.value })}
      />
      <button type="submit">Register</button>
    </form>
  );
};

export default Register;
