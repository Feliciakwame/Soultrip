import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./Components/Homepage";
import Login from "./Components/Login";
import Signup from "./Components/Signup";
import Navbar from "./Components/Navbar";
import Journal from "./Components/Journal";
import Profile from "./Components/Profile";
import Safety from "./Components/Safety";
import TrustedContacts from "./Components/TrustedContacts";
import React from "react";
function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/journal/:id" element={<Journal />} />
        <Route path="/profile/:id" element={<Profile />} />
        <Route path="/safety/:id" element={<Safety />} />
        <Route path="/trusted-contacts/:id" element={<TrustedContacts />} />
      </Routes>
    </Router>
  );
}

export default App;
