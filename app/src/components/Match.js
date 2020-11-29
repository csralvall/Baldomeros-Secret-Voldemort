import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Role from "./Role";
import Election from "./Election";
import MatchInfo from "./MatchInfo";
import Board from "./Board";
import Adivination from "./Adivination";
import Chat from "./Chat";
import "./css/Match.css";
import Expelliarmus from "./Expelliarmus";
import LeaveGame from "./LeaveGame";

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
      expelliarmus: "",
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
      {gameStatus.winner === "Voldemort is the director" ? (
        <div>
          <h1 className="winner-msg">The Death Eaters have won!</h1>
          <h2 className="winner-description">
            Voldemort has been chosen as director
          </h2>
        </div>
      ) : (
        ""
      )}
      {gameStatus.winner === "Voldemort died" ? (
        <div>
          <h1 className="winner-msg">The Order of The Phoenix has won!</h1>
          <h2 className="winner-description">Voldemort has died</h2>
        </div>
      ) : (
        ""
      )}
      {gameStatus.winner === "death eater" ? (
        <div>
          <h1 className="winner-msg">The Death Eaters have won!</h1>
          <h2 className="winner-description">
            They managed to enact six of their proclamations
          </h2>
        </div>
      ) : (
        ""
      )}
      {gameStatus.winner === "phoenix" ? (
        <div>
          <h1 className="winner-msg">The Order of The Phoenix has won!</h1>
          <h2 className="winner-description">
            They managed to enact five of their proclamations
          </h2>
        </div>
      ) : (
        ""
      )}
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
                  {gameStatus.matchstatus === "Closed" ? (
                    <LeaveGame status={gameStatus.matchstatus} />
                  ) : (
                    ""
                  )}
                </div>
                <div>
                  {gameStatus.matchstatus === "In Game" ? (
                    <Election
                      playerList={gameStatus.playerstatus}
                      minister={gameStatus.minister}
                      director={gameStatus.director}
                      candidate={gameStatus.candidate}
                      status={gameStatus.boardstatus.status}
                      hand={gameStatus.hand}
                      expelliarmus={gameStatus.boardstatus.expelliarmus}
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
                  {gameStatus.boardstatus.status === "expelliarmus" &&
                  gameStatus.minister === user.username ? (
                    <Expelliarmus
                      minister={gameStatus.minister}
                      director={gameStatus.director}
                      expelliarmus={gameStatus.boardstatus.expelliarmus}
                    />
                  ) : (
                    ""
                  )}
                  {gameStatus.boardstatus.expelliarmus === "unlocked" &&
                  gameStatus.boardstatus.status === "director selection" &&
                  gameStatus.director === user.username ? (
                    <Expelliarmus
                      minister={gameStatus.minister}
                      director={gameStatus.director}
                      expelliarmus={gameStatus.boardstatus.expelliarmus}
                    />
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
              <div>
                <Chat />
                <Board
                  phoenixProclamationCount={
                    gameStatus.boardstatus.phoenixproclamations
                  }
                  deathEaterProclamationCount={
                    gameStatus.boardstatus.deatheaterproclamations
                  }
                  chaosCirclePosition={gameStatus.boardstatus.failcounter}
                />
              </div>
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
