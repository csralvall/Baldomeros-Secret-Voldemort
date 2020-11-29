import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Role from "./Role";
import Election from "./Election";
import MatchInfo from "./MatchInfo";
import Board from "./Board";
import Adivination from "./Adivination";
import "./css/Match.css";

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
      failcounter: 0,
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
        }
      })
      .catch(() => {
        alert("Disconnected");
      });
  }, 1000);

  const Winner = (
    <div className="winner-div">
      <h1 className="winner-msg">The winner is {gameStatus.winner}</h1>
    </div>
  );

  //This needs a "Spell" component
  return (
    <div>
      {game.id === parseInt(match.params.id) ? (
        <div className="match">
          {gameStatus.matchstatus !== "Finished" ? (
            <div>
              <div className="match-left-top">
                <div className="title-and-game-id">
                  <h1 className="match-title"> {game.name} </h1>
                  <h4 className="game-id"> Game id : {game.id} </h4>
                </div>
              </div>
              <div className="match-left-bottom">
                {gameStatus.matchstatus === "Joinable" ? (
                  <div className="joinable-div">
                    <MatchInfo playerList={gameStatus.playerstatus} />
                  </div>
                ) : (
                  ""
                )}
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
                  {" "}
                  {gameStatus.matchstatus == "In Game" ? <Role /> : ""}{" "}
                </div>
                <div>
                  {gameStatus.boardstatus.spell === "Avada Kedavra" &&
                  gameStatus.boardstatus.status === "use spell" &&
                  gameStatus.minister === user.username ? (
                    <AvadaKedavra playerList={gameStatus.playerstatus} />
                  ) : (
                    ""
                  )}
                  {gameStatus.boardstatus.spell === "Adivination" &&
                  gameStatus.boardstatus.status === "use spell" &&
                  gameStatus.minister === user.username ? (
                    <Adivination hand={gameStatus.hand} />
                  ) : (
                    ""
                  )}
                </div>
              </div>
            </div>
          ) : (
            ""
          )}
          <div>
            {gameStatus.matchstatus === "Joinable" ||
            gameStatus.matchstatus === "In Game" ? (
              <Board
                phoenixProclamationCount={
                  gameStatus.boardstatus.phoenixproclamations
                }
                deathEaterProclamationCount={
                  gameStatus.boardstatus.deatheaterproclamations
                }
                boardType={gameStatus.boardstatus.boardtype}
                chaosCirclePosition={gameStatus.boardstatus.failcounter}
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
