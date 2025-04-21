import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser } from "../api/soultripAPI";
import "./Login.css";
import React from "react";

export default function Login() {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [errors, setErrors] = useState({});
  const navigate = useNavigate();

  const validate = () => {
    const newErrors = {};
    if (!formData.email) newErrors.email = "Email is required";
    if (!formData.password) newErrors.password = "Password is required";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    try {
      const response = await loginUser(formData);
      localStorage.setItem("authToken", response.data.token);
      navigate("/dashboard");
    } catch (err) {
      setErrors({ api: "Invalid credentials. Please try again." });
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h2 className="login-title">Log In to SoulTrip</h2>

        {errors.api && <div className="login-error">{errors.api}</div>}

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="email" className="input-label">
              Email
            </label>
            <input
              id="email"
              type="email"
              className={`login-input ${errors.email ? "input-error" : ""}`}
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
            />
            {errors.email && <span className="error-text">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password" className="input-label">
              Password
            </label>
            <input
              id="password"
              type="password"
              className={`login-input ${errors.password ? "input-error" : ""}`}
              value={formData.password}
              onChange={(e) =>
                setFormData({ ...formData, password: e.target.value })
              }
            />
            {errors.password && (
              <span className="error-text">{errors.password}</span>
            )}
          </div>

          <button type="submit" className="login-button">
            Log In
          </button>
        </form>

        <div className="login-footer">
          <p>
            Don't have an account?{" "}
            <Link to="/signup" className="auth-link">
              Sign up
            </Link>
          </p>
          <Link to="/forgot-password" className="forgot-password">
            Forgot password?
          </Link>
        </div>
      </div>
    </div>
  );
}
