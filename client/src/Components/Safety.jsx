import React, { useState, useEffect } from "react";
import "./Safety.css";

export default function Safety() {
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
          timeout: 10000,
          maximumAge: 0,
        }
      );

      return () => navigator.geolocation.clearWatch(watchId);
    } else {
      setError("Geolocation is not supported by your browser.");
    }
  }, []);

  const handleShare = () => {
    if (location.latitude && location.longitude) {
      console.log("Sending location to trusted contact...");
      // You’d replace this with a real API call
      setShared(true);
      setTimeout(() => setShared(false), 3000);
    } else {
      alert("Location not available yet!");
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
            <button className="share-button" onClick={handleShare}>
              📤 Share My Location
            </button>
            {shared && <p className="shared-confirm">Location shared ✅</p>}
          </>
        ) : (
          <p className="loading-text">Fetching location...</p>
        )}
      </div>
    </div>
  );
}
