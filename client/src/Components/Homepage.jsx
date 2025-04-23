import React from "react";
import "./Homepage.css";
import Footer from "./Footer";

function Homepage() {
  return (
    <div className="homepage">
      <div className="homepage-content">
        <h1>Welcome to SoulTrip 💫</h1>
        <p>Your safe space for solo travel, journaling & peace.</p>
      </div>
      <Footer />
    </div>
  );
}

export default Homepage;
