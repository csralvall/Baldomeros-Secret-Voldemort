import React,{useState} from "react";
import { useSelector, useDispatch} from "react-redux";
import {Link} from "react-router-dom";

function SignUp() {

  const [form,setForm] = useState(false);  

  return (
    <div>
      {form ? "Succesfully Registerd" :
        (
        <div>
          <h1> Register </h1>
          <h3>name</h3>
          <input type="text"/>
          <h3>password</h3>
          <input type="text"/>
          <h3>mail</h3>
          <input type="text"/>
          <button onClick = {() => setForm(true)}>Send</button>
        </div>
        )
      }
    </div>
  );
}
export default SignUp;
