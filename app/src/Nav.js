import React from "react";
import "./Nav.css";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";
import logo from "./media/SV_logo.png";

function Nav() {
  const logged_in = useSelector((state) => state.user.logged_in);
  return (
    <div>
      <nav>
        <img src={logo} className="nav-logo" alt="logo" />
        <ul className="nav-links">
          <Link to="/" className="nav-link">
            <li>Home</li>
          </Link>
          <Link to={!logged_in ? "/login" : "/Profile"} className="nav-link">
            <li>{!logged_in ? "Login" : "Profile"}</li>
          </Link>
          <Link to={!logged_in ? "/signup" : ""} className="nav-link">
            <li>{!logged_in ? "Sign Up" : ""}</li>
          </Link>
        </ul>
      </nav>
    </div>
  );
}

export default Nav;
