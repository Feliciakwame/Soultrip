import React, { useState, useEffect } from "react";
import "./Safety.css";
import LocationMap from "./LocationMap";

export default function Safety({ contacts }) {
  const [location, setLocation] = useState({ latitude: null, longitude: null });
  const [error, setError] = useState("");
  const [shared, setShared] = useState(false);

  useEffect(() => {
    if (navigator.geolocation) {
      const watchId = navigator.geolocation.watchPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
          setError("");
        },
        (err) => {
          console.error("Error fetching location:", err);
          setError("Unable to retrieve your location.");
        },
        {
          enableHighAccuracy: true,
          timeout: 30000,
          maximumAge: 0,
        }
      );

      return () => navigator.geolocation.clearWatch(watchId);
    } else {
      setError("Geolocation is not supported by your browser.");
    }
  }, []);

  const handleShare = async () => {
    if (location.latitude && location.longitude) {
      if (!contacts || contacts.length === 0) {
        alert("No trusted contacts available!");
        return;
      }

      try {
        const emailList = contacts.map((c) => c.email);
        const response = await fetch("http://localhost:5000/send-location", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            contacts,
            latitude: location.latitude,
            longitude: location.longitude,
          }),
        });

        if (!response.ok) throw new Error("Failed to send location");

        setShared(true);
        setTimeout(() => setShared(false), 3000);
      } catch (error) {
        alert("Error sending location via email.");
        console.error(error);
      }
    } else {
      alert("Location not available yet.");
    }
  };

  return (
    <div className="safety-container">
      <h2 className="safety-title">🛡️ Safety Dashboard</h2>
      <div className="location-card">
        <h3>📍 Live Location</h3>
        {error ? (
          <p className="error-text">{error}</p>
        ) : location.latitude && location.longitude ? (
          <>
            <p className="coordinates">
              Latitude: <span>{location.latitude.toFixed(5)}</span> <br />
              Longitude: <span>{location.longitude.toFixed(5)}</span>
            </p>

            <div className="map-container">
              <LocationMap
                latitude={location.latitude}
                longitude={location.longitude}
              />
            </div>

            <button className="share-button" onClick={handleShare}>
              📤 Share My Location
            </button>
            {shared && <p className="shared-confirm">Location shared ✅</p>}
            <p className="note-text">
              Your location is live and may be visible to your trusted contacts.
            </p>
          </>
        ) : (
          <p className="loading-text">Fetching location...</p>
        )}
      </div>
    </div>
  );
}
