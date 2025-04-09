import axios from "axios";

const API_BASE_URL = "http://localhost:8080";

export const api = {
  getInventory: async (filters) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/inventory`, { params: filters });
      return response.data;
    } catch (error) {
      console.error("Error fetching inventory:", error);
      throw error;
    }
  },
  createAlert: async (alertData, token) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/alerts`, alertData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      console.error("Error creating alert:", error);
      throw error;
    }
  },
  getSalesTrends: async (filters) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/sales-trends`, { params: filters });
      return response.data;
    } catch (error) {
      console.error("Error fetching sales trends:", error);
      throw error;
    }
  },
  login: async (credentials) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, credentials);
      return response.data;
    } catch (error) {
      console.error("Error logging in:", error);
      throw error;
    }
  },
  pushIntegration: async (integrationData, token) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/api/integration`, integrationData, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (error) {
      console.error("Error pushing integration data:", error);
      throw error;
    }
  },
};
