import axios from "axios";
import React, { useEffect, useState } from "react";
import { jwtDecode } from "jwt-decode";
import "./Profile.css";

function Profile() {
  const [user, setUser] = useState({
    username: "",
    email: "",
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({ ...user });

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const token = localStorage.getItem("authToken");
        const decoded = jwtDecode(token);
        const userId = decoded.sub || decoded.id;
        const response = await axios.get(
          `http://localhost:5000/api/users/${userId}`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        setUser(response.data);
        setEditedUser(response.data);
      } catch (err) {
        console.log("Error fetching your profile", err);
      }
    };
    fetchProfile();
  }, []);

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
      const decoded = jwtDecode(token);
      const userId = decoded.sub || decoded.id;
      const response = await axios.patch(
        `http://localhost:5000/api/users/${userId}`,
        editedUser,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setUser(response.data);
      setIsEditing(false);
    } catch (err) {
      console.log("Error saving your profile", err);
    }
  };

  return (
    <div className="profile-container">
      <h2>Your Profile</h2>
      <div className="profile-details">
        <img src={user.avatar} alt="Avatar" className="avatar" />
        <div className="user-info">
          {isEditing ? (
            <>
              <input
                type="text"
                name="name"
                value={editedUser.name}
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
                <strong>Name:</strong> {user.name}
              </p>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
            </>
          )}
        </div>
      </div>
      <button onClick={handleEditToggle}>
        {isEditing ? "Cancel" : "Edit Profile"}
      </button>
      {isEditing && <button onClick={handleSave}>Save Changes</button>}
    </div>
  );
}

export default Profile;
