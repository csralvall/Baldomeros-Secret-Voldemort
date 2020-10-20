import React from "react";
import {Link} from "react-router-dom";
function Register() {

  return (
    <div>
      <h1> Register </h1>
      <h3>name</h3>
      <h3>password</h3>
      <h3>mail</h3>
      <button>Send</button>
      <Link to= "/">
        <h2>Main page</h2>
      </Link>
    </div>
  );
}
export default Register;
