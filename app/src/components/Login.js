import React, {useState} from "react";
import { useSelector, useDispatch} from "react-redux";
import {useHistory} from "react-router-dom";
import { login } from "./../actions/login";

function Login() {
  
  const [user,setUser] = useState({username : "",password : ""});
  
  const changeUsername = (e) => { 
    setUser({username : e.target.value,
              password: user.password})
    }

  const changePassword = (e) => { 
    setUser({username : user.username,
              password: e.target.value})
    }
  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch();

  const history = useHistory();

  const handleClick = async () => {
    // const response = await fetch(
    //   'request' get {user}
    // )
    // const data = await response.json
    
    const data = user.username = "Tom Riddle" && user.password == "123"
    dispatch(login(data));
    if(data) history.push("/");
  }

  return (
    <div>
      <h3>Username</h3>
      <input value = {user.username} onChange = { e => (changeUsername(e))}/>
      <h3>Password</h3>
      <input value = {user.password} onChange = { e => (changePassword(e))}/>
      <button onClick={ () => {handleClick()}}>
        {logged_in ? "Logout" : "Login"}
      </button>
    </div>
  );
}
export default Login;