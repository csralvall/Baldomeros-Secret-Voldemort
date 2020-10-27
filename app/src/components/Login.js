import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { login } from "./../actions/login";

function Login() {

  const dispatch = useDispatch();
  const history = useHistory();

  const [userInput, setUser] = useState({ username: "", password: "" });

  const changeUsername = (e) => {
    setUser({
      username: e.target.value,
      password: userInput.password
    })
  }

  const changePassword = (e) => {
    setUser({
      username: userInput.username,
      password: e.target.value
    })
  }

  const autenticateUser = async (e) => {
    e.preventDefault();
    const url = "http://127.0.0.1:8000";

    const formData = new FormData();
    formData.append("username", userInput.username);
    formData.append("password", userInput.password);

    const response = await fetch(url + "/session", {
      method: "POST",
      body: formData,
    })
      .then(async (response) => {
        const responseData = await response.json()
        if (response.status !== 200) {
          if (response.status === 401) {
            alert("Username not found");
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

  }

  return (
    <div>
      <h1>Enter User Info</h1>
      <form onSubmit={autenticateUser}>
        <label>
          Username
          <input
            type="username"
            required
            value={userInput.username}
            onChange={changeUsername} />
        </label>
        <label>
          Password
          <input
            type="password"
            required
            value={userInput.password}
            onChange={changePassword} />
        </label>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
export default Login;