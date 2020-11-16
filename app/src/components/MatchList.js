import React, { useState } from "react";
import Modal from "react-modal";
import JoinMatch from "./JoinMatch";
import "./css/MatchList.css";
import cross from "../media/misc/cross.png";
import refresh from "../media/misc/refresh.png";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function MatchList() {
  const [gameList, setGameList] = useState([]);
  const [selectedGame, setSelectedGame] = useState(-1);
  const [open, setOpen] = useState(false);

  const getGames = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/list`, {
      method: "GET",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Match doesn't exist");
          } else {
            alert("Unknown Error.");
          }
        } else {
          setGameList(responseData);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div>
      <button
        onClick={() => {
          getGames();
          setOpen(true);
        }}
      >
        Join Match
      </button>
      <Modal
        isOpen={open}
        onRequestClose={() => {
          setOpen(false);
        }}
        closeTimeoutMS={200}
        style={{
          content: {
            position: "absolute",
            top: "50%",
            left: "50%",
            right: "auto",
            bottom: "auto",
            border: "1px solid #ccc",
            background: "#000",
            overflow: "auto",
            WebkitOverflowScrolling: "touch",
            borderRadius: "4px",
            outline: "none",
            padding: "20px",
            marginRight: "auto",
            transform: "translate(-50%, -50%)",
          },
        }}
      >
        <div>
          <img
            src={cross}
            className="quit"
            onClick={() => {
              setOpen(false);
            }}
          ></img>
          <img
            src={refresh}
            className="refresh"
            onClick={() => {
              getGames();
            }}
          ></img>

          <ul className="categories">
            <li>Nombre de la Partida</li>
            <li>Cantidad de jugadores</li>
          </ul>
          <ul className="matchList">
            {gameList.map((game, index) => (
              <li
                className={index === selectedGame ? "Selected" : "NotSelected"}
                onClick={() => {
                  setSelectedGame(index);
                }}
              >
                <ul className="entry">
                  <li>Partida de {game.Nombre_partida}</li>
                  <li>
                    {game.Min_and_Max[0]} - {game.Min_and_Max[1]}
                  </li>
                </ul>
              </li>
            ))}
          </ul>
          {selectedGame !== -1 ? (
            <JoinMatch matchID={gameList[selectedGame].Match_id} />
          ) : (
            ""
          )}
        </div>
      </Modal>
    </div>
  );
}

export default MatchList;
