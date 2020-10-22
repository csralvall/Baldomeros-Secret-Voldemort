import React, {useState} from "react";
import { useSelector, useDispatch} from "react-redux";
import {useHistory} from "react-router-dom";
import { login } from "./../actions/login";

function Login() {
  
  const [userInput,setUser] = useState({username : "",password : ""});
  
  const changeUsername = (e) => { 
    setUser({username : e.target.value,
              password: userInput.password})
    }

  const changePassword = (e) => { 
    setUser({username : userInput.username,
              password: e.target.value})
    }
  const logged_in = useSelector((state) => state.user.logged_in);
  const dispatch = useDispatch();

  const history = useHistory();

  const handleClick = async () => {
    // const response = await fetch(
    //   'request' get {user}
    // )
    // const data = await response.json
    
    const data = {logged_in : false, username : "Tom Riddle", id: 1};
    data.logged_in = userInput.username == "Tom Riddle" && userInput.password == "123"
    
    if(data.logged_in){
      dispatch(login(data));
      history.push("/");
    }
  }

  return (
    <div>
      <h3>Username</h3>
      <input value = {userInput.username} onChange = { e => (changeUsername(e))}/>
      <h3>Password</h3>
      <input value = {userInput.password} onChange = { e => (changePassword(e))}/>
      <button onClick={ () => {handleClick()}}>Login</button>
    </div>
  );
}
export default Login;