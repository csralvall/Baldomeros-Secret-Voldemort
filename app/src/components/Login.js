import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { login } from "./../actions/login";
import "./css/Login.css";

function Login() {
  const dispatch = useDispatch();
  const history = useHistory();

  const [userInput, setUser] = useState({ username: "", password: "" });

  const changeUsername = (e) => {
    setUser({
      username: e.target.value,
      password: userInput.password,
    });
  };

  const changePassword = (e) => {
    setUser({
      username: userInput.username,
      password: e.target.value,
    });
  };

  const autenticateUser = async (e) => {
    e.preventDefault();
    const url = "http://127.0.0.1:8000";

    const formData = new FormData();
    formData.append("username", userInput.username);
    formData.append("password", userInput.password);

    await fetch(url + "/session", {
      method: "POST",
      body: formData,
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 401) {
            alert("Username or password invalid.");
          } else {
            alert("Could not login. Unknown Error.");
          }
        } else {
          dispatch(login(responseData));
          history.push("/");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="log-in-module">
      <h1 className="log-in-title">Login</h1>
      <form onSubmit={autenticateUser} className="log-in-form">
        <label className="label-log-in">
          Username
          <input
            className="text-input"
            type="text"
            id="username"
            required
            value={userInput.username}
            onChange={changeUsername}
          />
        </label>
        <label className="label-log-in">
          Password
          <input
            className="text-input"
            type="password"
            required
            value={userInput.password}
            onChange={changePassword}
          />
        </label>
        <div className="button-log-in-wrapper">
          <button type="submit" className="button-log-in">
            Login
          </button>
        </div>
      </form>
    </div>
  );
}
export default Login;
