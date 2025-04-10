import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const login = async (username, password) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/login`, { username, password });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getInventory = async (filters = {}) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/inventory`, { params: filters });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const addInventory = async (inventory) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/inventory`, inventory);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getAlerts = async (filters = {}) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/alerts`, { params: filters });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const updateAlertThreshold = async (alertId, threshold) => {
  try {
    const response = await axios.put(`${API_BASE_URL}/alerts`, { alert_id: alertId, threshold });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getSalesTrends = async (filters) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/sales-trends`, { params: filters });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
