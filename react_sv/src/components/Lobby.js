import React from 'react';
import {useHistory} from "react-router-dom";
import Login from "./login";

function Lobby() {
  const history = useHistory();
function joinGame() {
    history.push("/match/1");
}

  const user = "Tom Riddle";
  return (
    <div >
      <Login/>
      <h1> Welcome, {user} </h1>
      <button>Create Game</button>
      <button onClick={() => {joinGame()}}>Join Game</button>
    </div>
  );
}

export default Lobby;
