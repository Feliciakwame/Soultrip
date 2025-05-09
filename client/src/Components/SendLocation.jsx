import React, { useState } from "react";

const SendLocation = () => {
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState("");

  const handleSendLocation = async () => {
    setSending(true);
    setMessage("");

    if (!navigator.geolocation) {
      setMessage("Geolocation is not supported by your browser.");
      setSending(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;

        // Replace with dynamic contacts if available
        const contacts = ["example1@gmail.com", "example2@gmail.com"];

        try {
          const response = await fetch("http://localhost:5000/send_location", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              contacts,
              latitude,
              longitude,
            }),
          });

          const data = await response.json();

          if (response.ok) {
            setMessage("📍 Location sent successfully!");
          } else {
            setMessage(`❌ Error: ${data.error}`);
          }
        } catch (error) {
          setMessage("Failed to send location.");
        } finally {
          setSending(false);
        }
      },
      (error) => {
        setMessage("Unable to get your location.");
        setSending(false);
      }
    );
  };

  return (
    <div>
      <h3>Send My Location</h3>
      <button onClick={handleSendLocation} disabled={sending}>
        {sending ? "Sending..." : "Send My Location via Email"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
};

export default SendLocation;
