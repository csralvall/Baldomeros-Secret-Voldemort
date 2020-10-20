import React from "react";
import {useRef} from "react";
import {useHistory} from "react-router-dom";
import Login from "./login";

function Register() {
 
const history = useHistory();

function handleClick() {
    history.push("/register");
}
  return (
    <div>
      <Login/>
      <h1> New? Try creating an account </h1>
      <button onClick = {() => {handleClick()}}> Register </button>
    </div>
  );
}
export default Register;
