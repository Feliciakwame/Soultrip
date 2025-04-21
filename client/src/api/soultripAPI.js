import axios from "axios";
const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});
export const loginUser = (credentials) => api.post("/login", credentials);
export const signupUser = (userData) => api.post("/signup", userData);

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});
export default api;
