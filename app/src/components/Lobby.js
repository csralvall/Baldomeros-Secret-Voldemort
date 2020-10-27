import React from 'react';
import JoinMatch from "./JoinMatch";
import {Link} from "react-router-dom";
import { useSelector} from "react-redux";

function Lobby() {

  //Esto vendría de useSelector
  const user = {username:"Tom Riddle",id:1,autenticator:true};
  const logged_in = useSelector((state) => state.user.logged_in);

  return (
    <div> 
      { logged_in ?
      (<div >
        <h1> Welcome, {user.username} </h1>
        <button>Create Game</button>
        <JoinMatch/>
      </div>)

      :

      (<div>
        <h1> You are not Logged In</h1>
        <Link to = "/login" >
        <h1> Login</h1>
        </Link>
      </div>)
      }
    </div>
  );
}

export default Lobby;
