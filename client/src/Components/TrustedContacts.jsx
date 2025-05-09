import React, { useState, useEffect } from "react";
import "./TrustedContacts.css";

export default function TrustedContacts() {
  const [contacts, setContacts] = useState([]);
  const [formData, setFormData] = useState({ name: "", phone: "", email: "" });
  const [editingId, setEditingId] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  useEffect(() => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      console.error("No authentication token found.");
      return;
    }

    fetch("http://localhost:5000/api/contacts", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP error! Status: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setContacts(data))
      .catch((err) => console.error("Error fetching contacts:", err));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddOrUpdate = async (e) => {
    e.preventDefault();

    const token = localStorage.getItem("authToken");
    if (!token) {
      setErrorMessage("No authentication token found.");
      return;
    }

    const url =
      editingId !== null
        ? `http://localhost:5000/api/contacts/${editingId}`
        : "http://localhost:5000/api/contacts";

    const method = editingId !== null ? "PUT" : "POST";

    const response = await fetch(url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(formData),
    });

    if (response.ok) {
      const result = await response.json();
      if (editingId !== null) {
        setContacts((prev) =>
          prev.map((c) => (c.id === result.id ? result : c))
        );
      } else {
        setContacts((prev) => [...prev, result]);
      }
      setFormData({ name: "", phone: "", email: "" });
      setEditingId(null);
      setErrorMessage("");
    } else {
      setErrorMessage("Failed to save contact.");
    }
  };

  const handleEdit = (contact) => {
    setFormData({
      name: contact.name,
      phone: contact.phone,
      email: contact.email,
    });
    setEditingId(contact.id);
  };

  const handleDelete = async (id) => {
    const token = localStorage.getItem("authToken");
    if (!token) {
      setErrorMessage("No authentication token found.");
      return;
    }

    const response = await fetch(`http://localhost:5000/api/contacts/${id}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.ok) {
      setContacts((prev) => prev.filter((c) => c.id !== id));
      setErrorMessage("");
    } else {
      setErrorMessage("Failed to delete contact.");
    }
  };

  const shareLocation = () => {
    if (contacts.length === 0) {
      alert("No trusted contacts to share with!");
      return;
    }

    const latitude = 0.3031;
    const longitude = 36.08;

    contacts.forEach((contact) => {
      console.log(`Sharing location with ${contact.name}`);
      console.log(
        `Send to ${contact.email}: I'm here 👉 https://maps.google.com/?q=${latitude},${longitude}`
      );
    });

    alert("Location shared with all trusted contacts! 💌");
  };

  return (
    <div className="trusted-container">
      <h2>👯‍♀️ Trusted Contacts</h2>

      {/* Error message */}
      {errorMessage && <p className="error-message">{errorMessage}</p>}

      <form onSubmit={handleAddOrUpdate} className="trusted-form">
        <input
          name="name"
          value={formData.name}
          onChange={handleChange}
          placeholder="Name"
          required
        />
        <input
          name="phone"
          value={formData.phone}
          onChange={handleChange}
          placeholder="Phone Number"
          required
        />
        <input
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
          required
        />
        <button type="submit">
          {editingId !== null ? "Update Contact" : "Add Contact"}
        </button>
      </form>

      <ul className="trusted-list">
        {contacts.map((contact) => (
          <li key={contact.id}>
            <div className="contact-details">
              <strong>{contact.name}</strong> <br />
              📞 {contact.phone} <br />
              📧 {contact.email}
            </div>
            <div className="contact-actions">
              <button onClick={() => handleEdit(contact)} className="edit-btn">
                ✏️ Edit
              </button>
              <button
                onClick={() => handleDelete(contact.id)}
                className="delete-btn"
              >
                🗑️ Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      <button onClick={shareLocation} className="share-location-btn">
        📤 Share My Location
      </button>
    </div>
  );
}
