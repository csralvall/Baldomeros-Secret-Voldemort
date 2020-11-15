import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Role from "./Role";
import Election from "./Election";
import MatchInfo from "./MatchInfo";
import Board from "./Board";

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
    winner: "",
    minister: "",
    candidate: "",
    playerstatus: {},
    hand: [],
  });

  useInterval(async () => {
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
          console.log(responseData);
        }
      })
      .catch(() => {
        alert("Disconnected");
      });
  }, 1000);

  const Winner = (
    <div>
      <h1>The winner is {gameStatus.winner}</h1>
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
                director={gameStatus.director}
                candidate={gameStatus.candidate}
                status={gameStatus.boardstatus.status}
                hand={gameStatus.hand}
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
          <div>
            {gameStatus.matchstatus === "In Game" ? (
              <Board
                phoenixProclamationCount={
                  gameStatus.boardstatus.phoenixproclamations
                }
                deathEaterProclamationCount={
                  gameStatus.boardstatus.deatheaterproclamations
                }
              />
            ) : (
              ""
            )}
          </div>
          <div> {gameStatus.matchstatus === "Finished" ? Winner : ""} </div>
        </div>
      ) : (
        <div> You didn't join this game </div>
      )}
    </div>
  );
}

export default Match;
