import axios from 'axios';

const API_URL = '/api/inventory';

export const getInventory = async (filters = {}) => {
  try {
    const response = await axios.get(API_URL, { params: filters });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const addInventory = async (item, token) => {
  try {
    const response = await axios.post(API_URL, item, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const updateInventory = async (id, item, token) => {
  try {
    const response = await axios.put(`${API_URL}/${id}`, item, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const deleteInventory = async (id, token) => {
  try {
    const response = await axios.delete(`${API_URL}/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};