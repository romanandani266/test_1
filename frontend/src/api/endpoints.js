import api from "./api";

export const login = (credentials) => api.post("/auth/login", credentials);
export const logout = () => api.post("/auth/logout");

export const getInventory = (params) => api.get("/inventory", { params });
export const addInventory = (data) => api.post("/inventory", data);
export const updateInventory = (id, data) => api.put(`/inventory/${id}`, data);
export const deleteInventory = (id) => api.delete(`/inventory/${id}`);

export const getAlerts = (params) => api.get("/alerts", { params });
export const createAlert = (data) => api.post("/alerts", data);
export const deleteAlert = (id) => api.delete(`/alerts/${id}`);

export const getSalesTrends = (params) => api.get("/sales/trends", { params });