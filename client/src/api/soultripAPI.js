import axios from "axios";

const baseURL = "http://localhost:5000/api";

const api = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("authToken");
  if (token) {
    config.headers["Authorization"] = `Bearer ${token}`;
  }
  return config;
});

export async function loginUser(userData) {
  const response = await api.post("/login", userData);
  return response.data;
}

export async function signupUser(userData) {
  const response = await api.post("/signup", userData);
  return response.data;
}

export default api;
