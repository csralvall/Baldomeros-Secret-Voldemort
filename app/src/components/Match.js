import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import Vote from "./Vote";

function Match({ match }) {
  const game = useSelector((state) => state.match);
  const user = useSelector((state) => state.user);
  const [gameStatus, setGameStatus] = useState({
    minister: "",
    players: {},
    matchstatus: "",
    phoenixproclamations: 0,
    deatheaterproclamations: 0,
    board_type: "5-6",
  });

  useInterval(async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/games/?mid=${game.id}`, {
      method: "GET",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Error");
          } else {
            alert("Unknown Error");
          }
        } else {
          setGameStatus(responseData);
        }
      })
      .catch(() => {
        alert("Disconnected");
      });
  }, 1000);

  const Election = (
    <div>
      <h1>The current minister is {gameStatus.minister}</h1>
      {Object.entries(gameStatus.players).map((player) => (
        <h4>
          {player[0]} voted {player[1]}
        </h4>
      ))}
      <div>
        {gameStatus.players[user.username] === "missing vote" ? <Vote /> : ""}
      </div>
    </div>
  );

  const Board = (
    <div>
      <h1>Phoenix Proclamations : {gameStatus.phoenixproclamations}/5</h1>
      <h1>
        Death Eaters Proclamations : {gameStatus.deatheaterproclamations}/6
      </h1>
    </div>
  );

  const Winner = (
    <div>
      <h1>
        {gameStatus.deatheaterproclamations > gameStatus.phoenixproclamations
          ? "Death Eaters"
          : "Order of the Phoenix"}{" "}
        team won the match
      </h1>
    </div>
  );

  const PlayerList = (
    <div>
      <h1>Players joined:</h1>
      {Object.entries(gameStatus.players).map((player) => (
        <h4>{player[0]}</h4>
      ))}
    </div>
  );

  return (
    <div>
      {game.id === parseInt(match.params.id) ? (
        <div>
          <h1> {game.name} </h1>
          <h4> Game id : {game.id} </h4>
          <h3> {user.id === game.hostId ? "You are the Host" : ""} </h3>
          <h2> {gameStatus.matchstatus === "Joinable" ? PlayerList : ""} </h2>
          <div> {gameStatus.matchstatus === "In Game" ? Election : ""} </div>
          <div> {gameStatus.matchstatus === "In Game" ? Board : ""} </div>
          <div> {gameStatus.matchstatus === "Finished" ? Winner : ""} </div>
        </div>
      ) : (
        <div> You didn't join this game </div>
      )}
    </div>
  );
}

export default Match;
