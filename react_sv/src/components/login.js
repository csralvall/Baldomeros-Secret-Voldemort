import React from "react";
import { useSelector, useDispatch} from "react-redux";
import {useHistory} from "react-router-dom";
import { login } from "./../actions/login";


function Login() {
  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch();
 
  const history = useHistory();

  function handleClick() {
    dispatch(login());
    if(!logged_in) history.push("/match");
    else history.push("/");
  }

  return (
    <div>
      <h3> {logged_in ? "Logged in!" : "Not logged in"} </h3>
      <button onClick={ () => {handleClick()}}>
        {logged_in ? "Logout" : "Login"}
      </button>
    </div>
  );
}
export default Login;
