import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080';

export const api = {
  getProducts: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/products`);
      return response.data;
    } catch (error) {
      console.error('Error fetching products:', error);
      throw error;
    }
  },
  getProduct: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/products/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching product:', error);
      throw error;
    }
  },
  addProduct: async (product) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/products`, product);
      return response.data;
    } catch (error) {
      console.error('Error adding product:', error);
      throw error;
    }
  },
  updateProduct: async (id, product) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/products/${id}`, product);
      return response.data;
    } catch (error) {
      console.error('Error updating product:', error);
      throw error;
    }
  },
  deleteProduct: async (id) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/products/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error deleting product:', error);
      throw error;
    }
  },
  getAlerts: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/alerts`);
      return response.data;
    } catch (error) {
      console.error('Error fetching alerts:', error);
      throw error;
    }
  },
  getSalesTrend: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sales-trends/${id}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching sales trend:', error);
      throw error;
    }
  },
  login: async (credentials) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/login`, credentials);
      return response.data;
    } catch (error) {
      console.error('Error logging in:', error);
      throw error;
    }
  },
};
