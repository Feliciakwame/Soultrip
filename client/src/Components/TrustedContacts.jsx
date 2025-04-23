import React, { useState, useEffect } from "react";
import "./TrustedContacts.css";
import LocationMap from "./LocationMap";

export default function TrustedContacts() {
  const [contacts, setContacts] = useState([]);
  const [formData, setFormData] = useState({ name: "", phone: "", email: "" });
  const [editingIndex, setEditingIndex] = useState(null);
  const [location, setLocation] = useState({ latitude: null, longitude: null });

  useEffect(() => {
    if (navigator.geolocation) {
      const watchId = navigator.geolocation.watchPosition(
        (pos) => {
          setLocation({
            latitude: pos.coords.latitude,
            longitude: pos.coords.longitude,
          });
        },
        (err) => {
          console.error("Location error:", err);
        },
        { enableHighAccuracy: true }
      );

      return () => navigator.geolocation.clearWatch(watchId);
    }
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleAddOrUpdate = (e) => {
    e.preventDefault();
    if (editingIndex !== null) {
      const updated = [...contacts];
      updated[editingIndex] = formData;
      setContacts(updated);
      setEditingIndex(null);
    } else {
      setContacts([...contacts, formData]);
    }
    setFormData({ name: "", phone: "", email: "" });
  };

  const handleEdit = (index) => {
    setFormData(contacts[index]);
    setEditingIndex(index);
  };

  const handleDelete = (index) => {
    const updated = contacts.filter((_, i) => i !== index);
    setContacts(updated);
    if (editingIndex === index) {
      setFormData({ name: "", phone: "", email: "" });
      setEditingIndex(null);
    }
  };

  const shareLocation = () => {
    if (contacts.length === 0) {
      alert("No trusted contacts to share with!");
      return;
    }

    if (!location.latitude || !location.longitude) {
      alert("Location not available.");
      return;
    }

    contacts.forEach((contact) => {
      console.log(`Sharing location with ${contact.name}`);
      console.log(
        `Send to ${contact.email}: I'm here 👉 https://maps.google.com/?q=${location.latitude},${location.longitude}`
      );
    });

    alert("Location shared with all trusted contacts! 💌");
  };

  return (
    <div className="trusted-container">
      <h2>Trusted Contacts</h2>
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
          {editingIndex !== null ? "Update Contact" : "Add Contact"}
        </button>
      </form>

      <ul className="trusted-list">
        {contacts.map((c, index) => (
          <li key={index}>
            <div className="contact-details">
              <strong>{c.name}</strong> <br />
              📞 {c.phone} <br />
              📧 {c.email}
            </div>
            <div className="contact-actions">
              <button onClick={() => handleEdit(index)} className="edit-btn">
                ✏️ Edit
              </button>
              <button
                onClick={() => handleDelete(index)}
                className="delete-btn"
              >
                🗑️ Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      <button onClick={shareLocation} className="share-location-btn">
        📍 Share My Location
      </button>
      <div className="map-section">
        <h3>🗺️ Your Location on the map</h3>
        <LocationMap />
      </div>
    </div>
  );
}
