import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, {
      username,
      password,
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || error.message || "Login failed");
  }
};

export const getInventory = async (token) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inventory`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || error.message || "Failed to fetch inventory");
  }
};

export const addInventory = async (item, token) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/inventory`, item, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || error.message || "Failed to add inventory");
  }
};