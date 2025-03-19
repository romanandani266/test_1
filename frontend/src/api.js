import axios from "axios";

const API_URL = "http://localhost:8080";

export const fetchBlogs = async () => {
  try {
    const response = await axios.get(`${API_URL}/blogs`);
    return response.data;
  } catch (error) {
    console.error("Error fetching blogs:", error);
    throw error;
  }
};

export const fetchBlogById = async (id) => {
  try {
    const response = await axios.get(`${API_URL}/blogs/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching blog:", error);
    throw error;
  }
};

export const createBlog = async (blog) => {
  try {
    const response = await axios.post(`${API_URL}/blogs`, blog);
    return response.data;
  } catch (error) {
    console.error("Error creating blog:", error);
    throw error;
  }
};

export const updateBlog = async (id, blog) => {
  try {
    const response = await axios.put(`${API_URL}/blogs/${id}`, blog);
    return response.data;
  } catch (error) {
    console.error("Error updating blog:", error);
    throw error;
  }
};

export const deleteBlog = async (id) => {
  try {
    const response = await axios.delete(`${API_URL}/blogs/${id}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting blog:", error);
    throw error;
  }
};
