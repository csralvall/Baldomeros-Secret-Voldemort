import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { signUp } from "./../actions/signUpAction";

function SignUp() {
  const [userProps, setUserProps] = useState({
    username: "",
    password: "",
    email: "",
  });

  const updateUsername = (e) => {
    setUserProps({
      username: e.target.value,
      password: userProps.password,
      email: userProps.email,
    });
  };

  const updatePassword = (e) => {
    setUserProps({
      username: userProps.username,
      password: e.target.value,
      email: userProps.email,
    });
  };

  const updateEmail = (e) => {
    setUserProps({
      username: userProps.username,
      password: userProps.password,
      email: e.target.value,
    });
  };

  const dispatch = useDispatch();

  const getUserProps = (e) => {
    e.preventDefault();
    dispatch(signUp());
    console.log(userProps);
  };

  const hasSignedUp = useSelector((state) => state.hasSignedUp);

  return (
    <div>
      {hasSignedUp ? (
        <h1>Succesfully Registered</h1>
      ) : (
        <div>
          <h1>Sign Up</h1>
          <form onSubmit={getUserProps}>
            <label>
              Username
              <input
                className="text-input"
                type="text"
                value={userProps.username}
                onChange={updateUsername}
                required
              />
            </label>
            <label>
              Password
              <input
                className="text-input"
                type="password"
                value={userProps.password}
                onChange={updatePassword}
                required
              />
            </label>
            <label>
              E-Mail
              <input
                className="text-input"
                type="email"
                value={userProps.email}
                onChange={updateEmail}
                required
              />
            </label>
            <button type="submit">Sign Up!</button>
          </form>
        </div>
      )}
    </div>
  );
}
export default SignUp;
