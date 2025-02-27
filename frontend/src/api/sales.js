import axios from 'axios';

const API_URL = '/api/sales/trends';

export const getSalesTrends = async (filters = {}) => {
  try {
    const response = await axios.get(API_URL, { params: filters });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};