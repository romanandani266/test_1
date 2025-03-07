import axios from 'axios';

// Base URL for authentication-related API endpoints
const API_URL = '/api/auth';

// Function to handle user login
export const login = async (username, password) => {
  try {
    // Sending a POST request to the login endpoint with username and password
    const response = await axios.post(`${API_URL}/login`, { username, password });
    // Returning the response data from the server
    return response.data;
  } catch (error) {
    // Throwing the error response data if the request fails
    throw error.response.data;
  }
};

// Function to handle user logout
export const logout = async (token) => {
  try {
    // Sending a POST request to the logout endpoint with authorization header
    const response = await axios.post(`${API_URL}/logout`, {}, {
      headers: { Authorization: `Bearer ${token}` },
    });
    // Returning the response data from the server
    return response.data;
  } catch (error) {
    // Throwing the error response data if the request fails
    throw error.response.data;
  }
};