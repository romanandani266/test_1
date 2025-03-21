import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/auth/login`, credentials);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const fetchInventory = async (token) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inventory`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const createRestockingAlert = async (alert, token) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/alerts/restocking`, alert, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const fetchSalesTrends = async (params, token) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sales/trends`, {
      params,
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const sendNotification = async (notification, token) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/notifications`, notification, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
