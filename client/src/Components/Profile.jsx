import React, { useEffect, useState } from "react";
import "./Profile.css";

function Profile() {
  const [user, setUser] = useState({
    name: "",
    email: "",
    avatar: "",
  });

  const [isEditing, setIsEditing] = useState(false);
  const [editedUser, setEditedUser] = useState({ ...user });

  useEffect(() => {
    fetch("/profile")
      .then((res) => res.json())
      .then((data) => {
        if (!data.error) {
          setUser(data);
          setEditedUser(data);
        }
      })
      .catch((error) => {
        console.error("Error fetching user data:", error);
      });
  }, []); // ← Don't forget the empty dependency array

  const handleEditToggle = () => {
    setIsEditing(!isEditing);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEditedUser({ ...editedUser, [name]: value });
  };

  const handleSave = () => {
    fetch("/profile", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editedUser),
    })
      .then((res) => res.json())
      .then((updatedUser) => {
        setUser(updatedUser);
        setIsEditing(false);
      })
      .catch((err) => console.log("Error saving your profile", err));
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
