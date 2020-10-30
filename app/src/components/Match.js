import React from 'react';
import { useSelector, useDispatch} from "react-redux";


function Match( {match} ) {

  const game = useSelector(state => state.match);
  const user = useSelector((state) => state.user);
  
  const gameStatus = 
  {'minister': 'mati', 
  'players': [{name: 'mati', vote:'lumos'},
              {name: 'manu', vote:'lumos'},
              {name: 'cesar', vote:'nox'},
              {name: 'guido', vote:'nox'},
              {name: 'joaquin', vote:'missing'},
              {name: 'rodri', vote:'missing'}],
  'status': 'Started', 
  'board': {'PhoenixProclamations': 1, 'DeathEaterProclamations': 4, 'board_type': '5-6'},
  'winner': 'Death Eaters'}

  const myPlayer = gameStatus.players.find(player =>(
    player.name === user.username
  ))

  const Election = (
    <div>
      <h1>The current minister is {gameStatus.minister}</h1>    
      {gameStatus.players.map(player =>(
        <h4>Player {player.name} voted {player.vote}</h4>
      ))}
      <div> { myPlayer.vote === 'missing' ? (<button> Vote </button>) : ""}</div>
    </div>
  )

  const Board = (
    <div>
      <h1> Phoenix Proclamations : {gameStatus.board.PhoenixProclamations}/5 </h1>
      <h1> Death Eaters Proclamations : {gameStatus.board.DeathEaterProclamations}/6 </h1>
    </div>
  )

  const Winner = (
    <div>
      <h1> {gameStatus.winner} team won the match</h1>
    </div>
  )

  return (
    <div>
      {game.id == match.params.id ? 
      (<div>
      <h1> {game.name} </h1>
      <h4> Game id : {game.id} </h4>
      <h3> {user.id == game.hostId ? "You are the Host" : "" } </h3>
      <div> {gameStatus.status === 'Started' ? Election : ""} </div>
      <div> {gameStatus.status === 'Started' ? Board : ""} </div>
      <div> {gameStatus.status === 'Finished' ? Winner : ""} </div>
      </div>)
      :
      (<div> You didn't join this game </div>)}
    </div>
  );
}

export default Match;
