import React, {useState} from "react";
import { useSelector, useDispatch} from "react-redux";
import {useHistory} from "react-router-dom";
import { login } from "./../actions/login";

function Login() {
  

  //Repetir para contraseña
  //Hacer un componente que tenga esto no sería una mala idea
  const [usernameInput,setUsernameInput] = useState('');
  const changeInput = e => (
    setUsernameInput(e.target.value)
  )


  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch();
 
  const history = useHistory();

  function handleClick() {
    dispatch(login());
    if(!logged_in) history.push("/");
    else history.push("/");
  }

  return (
    <div>
      <h3>Username</h3>
      <input value = {usernameInput} onChange = { e => (changeInput(e))}/>
      <h3>Password</h3>
      <input passwordInput/>
      <button onClick={ () => {handleClick()}}>
        {logged_in ? "Logout" : "Login"}
      </button>
    </div>
  );
}
export default Login;