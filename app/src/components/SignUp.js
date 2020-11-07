import React, { useEffect, useState, useRef } from "react";
import { useHistory } from "react-router-dom";
import "./css/SignUp.css";

function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [userProps, setUserProps] = useState({});
  const history = useHistory();

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      registerUser();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [userProps]);

  const updateUsername = (e) => {
    setUsername(e.target.value);
  };

  const updatePassword = (e) => {
    setPassword(e.target.value);
  };

  const updateEmail = (e) => {
    setEmail(e.target.value);
  };

  const registerUser = async () => {
    const url = "http://127.0.0.1:8000";

    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    formData.append("email", email);

    await fetch(url + "/account", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.status !== 201) {
          if (response.status === 409) {
            alert("Username or E-Mail already exist");
          } else {
            alert("Could not Sign Up. Unknown Error.");
          }
        } else {
          history.push("/login");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const getUserProps = (e) => {
    e.preventDefault();
    setUserProps({
      username: username,
      password: password,
      email: email,
    });
  };

  return (
    <div className="sign-up-module">
      <h1 className="sign-up-title">Sign Up</h1>
      <form onSubmit={getUserProps} className="sign-up-form">
        <label className="label-sign-up">
          Username
          <input
            className="text-input"
            type="text"
            value={username}
            onChange={updateUsername}
            required
          />
        </label>
        <label className="label-sign-up">
          Password
          <input
            className="text-input"
            type="password"
            value={password}
            onChange={updatePassword}
            required
          />
        </label>
        <label className="label-sign-up">
          E-Mail
          <input
            className="text-input"
            type="email"
            value={email}
            onChange={updateEmail}
            required
          />
        </label>
        <div className="button-sign-up-wrapper">
          <button type="submit" className="button-sign-up">
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
}

export default SignUp;
