import React from 'react';
import {useHistory, Link} from "react-router-dom";
import { useSelector, useDispatch} from "react-redux";

function Lobby() {

  const user = "Tom Riddle";
  const logged_in = useSelector((state) => state.user.logged_in);


  const history = useHistory(); 

  function joinGame() {
      history.push("/match/1");
    }

  return (
    <div> 
      { logged_in ?
      (<div >
        <h1> Welcome, {user} </h1>
        <button>Create Game</button>
        <button onClick={() => {joinGame()}}>Join Game</button>
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
