import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom"; // Import Link for navigation
import { jwtDecode } from "jwt-decode";
import "./Profile.css";

export default function Profile() {
  const [user, setUser] = useState({
    username: "",
    email: "",
    avatar: "", // Assuming you have an avatar field in your backend
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({ ...user });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("authToken");
        if (!token) {
          console.error("No token found, user not authenticated.");
          return;
        }

        const decoded = jwtDecode(token);
        const userId = decoded.sub || decoded.id; // Extract user ID from token

        // Fetch user profile based on the user ID
        const response = await axios.get(
          `http://localhost:5000/api/profile/${userId}`,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        setUser(response.data);
        setEditedUser(response.data); // Initialize the edited user state with the profile data
      } catch (err) {
        console.error("Error fetching your profile:", err);
      }
    };

    fetchProfile();
  }, []); // Empty dependency array means this effect runs only once after the initial render

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedUser({ ...editedUser, [name]: value });
  };

  const handleSave = async () => {
    try {
      const token = localStorage.getItem("authToken");
      if (!token) {
        console.error("No token found, user not authenticated.");
        return;
      }

      const response = await axios.patch(
        `http://localhost:5000/api/profile/update`,
        editedUser,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setUser(response.data);
      setIsEditing(false);
    } catch (err) {
      console.error("Error saving your profile", err);
    }
  };

  return (
    <div className="profile-container">
      <h2>Your Profile</h2>
      <div className="profile-details">
        <img
          src={user.avatar || "https://via.placeholder.com/150"}
          alt="Avatar"
          className="avatar"
        />
        <div className="user-info">
          {isEditing ? (
            <>
              <input
                type="text"
                name="username"
                value={editedUser.username}
                onChange={handleInputChange}
              />
              <input
                type="email"
                name="email"
                value={editedUser.email}
                onChange={handleInputChange}
              />
            </>
          ) : (
            <>
              <p>
                <strong>Username:</strong> {user.username}
              </p>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
            </>
          )}
        </div>
      </div>

      <div className="profile-links">
        <Link to={`/journal/${user.username}`} className="profile-link">
          📖 View Journal
        </Link>
        <Link to={`/safety/${user.username}`} className="profile-link">
          🛡️ Safety
        </Link>
        <Link
          to={`/trusted-contacts/${user.username}`}
          className="profile-link"
        >
          👥 Trusted Contacts
        </Link>
      </div>

      <button onClick={handleEditToggle}>
        {isEditing ? "Cancel" : "Edit Profile"}
      </button>
      {isEditing && <button onClick={handleSave}>Save Changes</button>}
    </div>
  );
}
