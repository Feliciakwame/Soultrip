import React from "react";
import "./Homepage.css";
import Footer from "./Footer";

function Homepage() {
  return (
    <div className="homepage">
      <div className="homepage-image-wrapper">
        <img
          src="https://i.fbcd.co/products/original/70328853c33476d6c98831820bcf841a8368deebe619a21cfd7688560f0d46cd.jpg"
          alt="Peaceful solo traveler"
          className="homepage-image"
        />
        <div className="homepage-content">
          <h1>Welcome to SoulTrip 💫</h1>
          <p>Your safe space for solo travel, journaling & peace.</p>
        </div>
      </div>
      <Footer />
    </div>
  );
}

export default Homepage;
