import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Role from "./Role";
import Election from "./Election";
import MatchInfo from "./MatchInfo";

function Match({ match }) {
  const game = useSelector((state) => state.match);
  const user = useSelector((state) => state.user);
  const [gameStatus, setGameStatus] = useState({
    boardstatus: {
      boardtype: "",
      deatheaterproclamations: 0,
      phoenixproclamations: 0,
      spell: null,
      status: "",
    },
    matchstatus: "",
    minister: "",
    playerstatus: {},
  });

  const gamestatus = useInterval(async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${game.id}`, {
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

  //If this component grows more complex, separate it
  const Board = (
    <div>
      <h1>
        Phoenix Proclamations : {gameStatus.boardstatus.phoenixproclamations}/5
      </h1>
      <h1>
        Death Eaters Proclamations :{" "}
        {gameStatus.boardstatus.deatheaterproclamations}/6
      </h1>
    </div>
  );

  //This should come with status
  const Winner = (
    <div>
      <h1>
        {gameStatus.boardstatus.deatheaterproclamations >
        gameStatus.boardstatus.phoenixproclamations
          ? "Death Eaters"
          : "Order of the Phoenix"}{" "}
        team won the match
      </h1>
    </div>
  );

  return (
    <div>
      {game.id === parseInt(match.params.id) ? (
        <div>
          <h1> {game.name} </h1>
          <h4> Game id : {game.id} </h4>
          <h3>
            {gameStatus.matchstatus === "Joinable" ? (
              <MatchInfo playerList={gameStatus.playerstatus} />
            ) : (
              ""
            )}
          </h3>
          <div> {gameStatus.matchstatus == "In Game" ? <Role /> : ""} </div>
          <div>
            {gameStatus.matchstatus === "In Game" ? (
              <Election
                playerList={gameStatus.playerstatus}
                minister={gameStatus.minister}
              />
            ) : (
              ""
            )}
          </div>
          <div>
            {gameStatus.boardstatus.spell === "Avada Kedavra" &&
            gameStatus.boardstatus.status === "use spell" &&
            gameStatus.minister === user.username ? (
              <AvadaKedavra playerList={gameStatus.playerstatus} />
            ) : (
              ""
            )}
          </div>
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
