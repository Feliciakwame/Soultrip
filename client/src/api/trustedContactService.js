import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Create a trusted contact
export const createContact = async (contactData) => {
  const response = await api.post("/contacts", contactData);
  return response.data;
};

// Get all trusted contacts
export const getContacts = async () => {
  const response = await api.get("/contacts");
  return response.data;
};

// Get a single trusted contact by ID
export const getContactById = async (contactId) => {
  const response = await api.get(`/contacts/${contactId}`);
  return response.data;
};

// Update a trusted contact
export const updateContact = async (contactId, updateData) => {
  const response = await api.put(`/contacts/${contactId}`, updateData);
  return response.data;
};

// Delete a trusted contact
export const deleteContact = async (contactId) => {
  const response = await api.delete(`/contacts/${contactId}`);
  return response.data;
};

// Search contacts by query (name or email)
export const searchContacts = async (query) => {
  const response = await api.get(
    `/contacts/search?query=${encodeURIComponent(query)}`
  );
  return response.data;
};

// Notify emergency contacts (send emergency message and location)
export const notifyEmergencyContacts = async ({ location, message }) => {
  const response = await api.post("/emergency/notify", { location, message });
  return response.data;
};
