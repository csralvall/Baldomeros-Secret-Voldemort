import React, { useEffect, useState, useRef } from "react";

function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [userProps, setUserProps] = useState({});
  const [isSignUpSuccess, setIsSignUpSuccess] = useState(false);

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      registerUser();
    } else {
      loaded.current = true;
    }
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

    const response = await fetch(url + "/account", {
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
          setIsSignUpSuccess(true);
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

  const signUpFormJSX = (
    <div>
      <h1>Sign Up</h1>
      <form onSubmit={getUserProps}>
        <label>
          Username
          <input
            className="text-input"
            type="text"
            value={username}
            onChange={updateUsername}
            required
          />
        </label>
        <label>
          Password
          <input
            className="text-input"
            type="password"
            value={password}
            onChange={updatePassword}
            required
          />
        </label>
        <label>
          E-Mail
          <input
            className="text-input"
            type="email"
            value={email}
            onChange={updateEmail}
            required
          />
        </label>
        <button type="submit">Sign Up!</button>
      </form>
    </div>
  );

  return <div>{isSignUpSuccess ? <h1>Success!</h1> : signUpFormJSX}</div>;
}

export default SignUp;
