import React from "react";
import "./css/Nav.css";
import { Link } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import logo from "../media/logos/logo.png";
import { logout } from "../actions/login";

function Nav() {
  const logged_in = useSelector((state) => state.user.logged_in);
  const dispatch = useDispatch();
  const handleLogout = () => {
    if (logged_in) {
      dispatch(logout());
    }
  };
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
          <Link to={!logged_in ? "/signup" : "/"} className="nav-link">
            <li onClick={handleLogout}>{!logged_in ? "Sign Up" : "Log Out"}</li>
          </Link>
        </ul>
      </nav>
    </div>
  );
}

export default Nav;
