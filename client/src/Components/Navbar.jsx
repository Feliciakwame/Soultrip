import { Link } from "react-router-dom";
import "./Navbar.css";
import React from "react";

function Navbar() {
  return (
    <nav>
      <Link to="/">Home</Link>
      <Link to="/login">Login</Link>
      <Link to="/signup">Sign Up</Link>
      <Link to="/profile">Profile</Link>
      <Link to="/journal">Journal</Link>
      <Link to="/safety">Safety</Link>
    </nav>
  );
}
export default Navbar;
