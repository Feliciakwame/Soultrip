import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Create a new journal entry
export const createJournalEntry = async (data) => {
  const response = await api.post("/journal", data);
  return response.data;
};

// Get all journal entries (optionally with a limit)
export const getJournalEntries = async (limit = null) => {
  const params = limit ? { limit } : {};
  const response = await api.get("/journal", { params });
  return response.data;
};

// Get a single journal entry by ID
export const getJournalEntry = async (entryId) => {
  const response = await api.get(`/journal/${entryId}`);
  return response.data;
};

// Update a journal entry
export const updateJournalEntry = async (entryId, data) => {
  const response = await api.put(`/journal/${entryId}`, data);
  return response.data;
};

// Delete a journal entry
export const deleteJournalEntry = async (entryId) => {
  const response = await api.delete(`/journal/${entryId}`);
  return response.data;
};

// Search journal entries by query (title or content)
export const searchJournalEntries = async (query) => {
  const response = await api.get("/journal/search", {
    params: { query },
  });
  return response.data;
};

// Get journal statistics
export const getJournalStats = async () => {
  const response = await api.get("/journal/stats");
  return response.data;
};
