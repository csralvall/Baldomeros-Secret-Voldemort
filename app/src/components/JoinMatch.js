import React from "react";
import { useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { joinMatch } from "../actions/match";
import "./css/MatchList.css";

function JoinMatch({ matchID }) {
  const dispatch = useDispatch();
  const history = useHistory();
  const user = useSelector((state) => state.user);
  const joinGame = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}?user=${user.id}`, {
      method: "POST",
      //body: formData,
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Could not join");
          } else {
            alert("Could not join. Unknown Error.");
          }
        } else {
          dispatch(joinMatch(responseData));
          history.push("/match/" + responseData.Match_id);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };
  return (
    <div
      className="join"
      onClick={() => {
        joinGame();
      }}
    >
      Join Match
    </div>
  );
}

export default JoinMatch;
