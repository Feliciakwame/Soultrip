import React from "react";
import "./Homepage.css";
import Footer from "./Footer";
function Homepage() {
  return (
    <div className="homepage">
      <div className="overlay">
        <h1 className="homepage-title">💗 Welcome to SoulTrip 💗</h1>
        <p className="homepage-subtext">
          Your safe space to plan,journal and sparkle through your solo journey.
        </p>
      </div>
      <Footer />
    </div>
  );
}
export default Homepage;
