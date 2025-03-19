import axios from "axios";

const API_BASE_URL = "http://localhost:8080/api";

export const api = {
  login: (data) => axios.post(`${API_BASE_URL}/login`, data),
  getInventory: () => axios.get(`${API_BASE_URL}/inventory`),
  updateInventory: (data) => axios.put(`${API_BASE_URL}/inventory`, data),
  addProduct: (data) => axios.post(`${API_BASE_URL}/inventory`, data),
  deleteProduct: (productId) => axios.delete(`${API_BASE_URL}/inventory/${productId}`),
  getSalesTrends: () => axios.get(`${API_BASE_URL}/sales-trends`),
  getNotifications: () => axios.get(`${API_BASE_URL}/notifications`),
};
