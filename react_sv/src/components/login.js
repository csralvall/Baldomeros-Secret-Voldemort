import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { login } from "./../actions/login";

function Login() {
  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch();

  return (
    <div>
      <h1> {logged_in ? "Logged in!" : "Not logged in"} </h1>
      <button onClick={() => dispatch(login())}>
        {logged_in ? "Logout" : "Login"}
      </button>
    </div>
  );
}
export default Login;
