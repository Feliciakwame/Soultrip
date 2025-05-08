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
  return await axios.post(`${baseURL}/login`, userData);
}

export const signupUser = (formData) => {
  return axios.post("http://localhost:5000/api/signup", formData, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export default api;
