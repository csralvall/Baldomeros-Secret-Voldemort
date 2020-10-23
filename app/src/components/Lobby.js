import React from 'react';
import {useHistory, Link} from "react-router-dom";
import { useSelector, useDispatch} from "react-redux";
import {joinMatch} from "./../actions/match"

function Lobby() {

  //Esto vendría de useSelector
  const user = {username:"Tom Riddle",id:1};
  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch()

  const history = useHistory(); 

  const joinGame = async () => {
    // const response = await fetch(
    //   'request'
    // )
    // const matchData = await response.json
    // IF (200 ok)
    const matchData = {id : 1, name : "Mesa uno", hostid : 1,
    userlist : ["player 1", "player 2", "player 3", "player 4", "player 5", "Tom Riddle"]}
    dispatch(joinMatch(matchData));
    history.push("/match/"+matchData.id);
  }

  return (
    <div> { logged_in ?
      (<div >
        <h1> Welcome, {user.username} </h1>
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
