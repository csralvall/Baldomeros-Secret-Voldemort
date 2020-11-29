import React from "react";
import { useSelector, useDispatch } from "react-redux";
import { useHistory } from "react-router-dom";
import { leaveMatchAction } from "../actions/match";
import "./css/MatchInfo.css";

function LeaveGame({ status }) {
  const playerID = useSelector((state) => state.match.playerId);
  const matchID = useSelector((state) => state.match.id);
  const dispatch = useDispatch();
  const history = useHistory();

  const leave = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}/leave/${playerID}`, {
      method: "PATCH",
    })
      .then(async (response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Could not leave");
          } else {
            alert("Could not leave. Unknown Error.");
          }
        } else {
          dispatch(leaveMatchAction());
          history.push("/");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="joinable-info">
      {status === "Joinable" ? (
        <button className="start-btn" onClick={() => leave()}>
          Leave Game
        </button>
      ) : (
        <button
          className="start-btn"
          onClick={() => {
            dispatch(leaveMatchAction());
            history.push("/");
          }}
        >
          Leave Game
        </button>
      )}
    </div>
  );
}

export default LeaveGame;
