import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import Vote from "./Vote";
import AvadaKedavra from "./AvadaKedavra";

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

  function getPlayerVote() {
    if (gameStatus.matchstatus !== "")
      if (!gameStatus.playerstatus[user.username].isDead)
        return gameStatus.playerstatus[user.username].vote;
    return "";
  }

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

  const startGame = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + "/game/" + game.id + "?user=" + user.id, {
      method: "PATCH",
    })
      .then((response) => {
        console.log(response);
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Unable to start");
          } else {
            alert("Unknown error");
          }
        } else {
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const Election = (
    <div>
      <h1>The current minister is {gameStatus.minister}</h1>
      {Object.entries(gameStatus.playerstatus).map((player) => (
        <h4>
          {player[1].isDead ? "" : player[0] + " voted " + player[1].vote}
        </h4>
      ))}
      <div>{getPlayerVote() === "missing vote" ? <Vote /> : ""}</div>
    </div>
  );

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

  const PlayerList = (
    <div>
      <h1>Players joined:</h1>
      {Object.entries(gameStatus.playerstatus).map((player) => (
        <h4>{player[0]}</h4>
      ))}
    </div>
  );

  const Host = (
    <div>
      {user.id === game.hostId ? (
        <div>
          <h3>You are the host</h3>
          <button
            onClick={() => {
              startGame();
            }}
          >
            Start Game
          </button>
        </div>
      ) : (
        <h3>Waiting for Host to start the game</h3>
      )}
    </div>
  );

  return (
    <div>
      {game.id === parseInt(match.params.id) ? (
        <div>
          <h1> {game.name} </h1>
          <h4> Game id : {game.id} </h4>
          <h3> {gameStatus.matchstatus === "Joinable" ? Host : ""} </h3>
          <h2> {gameStatus.matchstatus === "Joinable" ? PlayerList : ""} </h2>
          <div> {gameStatus.matchstatus === "In Game" ? Election : ""} </div>
          <div>
            {
              /* {gameStatus.boardstatus.spell === "Avada-Kedavra" &&
            gameStatus.minister === user.username ? (
              <AvadaKedavra playerList={gameStatus.playerstatus} />
            ) : (
              ""
            )} */
              gameStatus.boardstatus.deatheaterproclamations === 5 &&
              gameStatus.minister === user.username ? (
                <AvadaKedavra playerList={gameStatus.playerstatus} />
              ) : (
                ""
              )
            }
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
