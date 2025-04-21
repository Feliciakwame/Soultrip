import React from "react";

import "./Safety.css";

export default function Safety() {
  const handleCheckIn = () => {
    alert("✅ You’ve checked in safely!");
  };

  const handleEmergency = () => {
    alert("🚨 Emergency alert sent to your trusted contacts!");
  };

  return (
    <div className="safety-container">
      <h2>🛡️ Safety Center</h2>
      <p className="subtitle">
        Keep your trusted circle updated and stay safe 💕
      </p>

      <div className="safety-buttons">
        <button onClick={handleCheckIn} className="check-in-btn">
          ✅ I’m Safe
        </button>
        <button onClick={handleEmergency} className="emergency-btn">
          🚨 Emergency
        </button>
      </div>

      <div className="safety-info">
        <p>
          <strong>🔒 Location sharing:</strong> ON
        </p>
        <p>
          <strong>📍 Last known location:</strong> Nairobi, Kenya
        </p>
        <p>
          <strong>👩‍❤️‍👨 Trusted Contacts:</strong> 2
        </p>
      </div>
    </div>
  );
}
